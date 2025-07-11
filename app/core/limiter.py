from app.redis import redis_client
from fastapi import HTTPException
from typing import Optional
from redis.exceptions import RedisError
from app.models.request_model import RateLimitCheckResponse

def get_policy_for(api_key: str, route_key: str, role: Optional[str]):
    try:
        r = redis_client.get_client()
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    redis_key = f"policy:{api_key}:{route_key}:{role}"
    policy = r.hgetall(redis_key)

    if not policy:
        raise HTTPException(status_code=404, detail="Rate limit policy not found")

    try:
        return {
            "limit": int(policy["limit"]),
            "window_seconds": int(policy["window"]),
            "is_active": bool(int(policy.get("is_active", "1")))
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Malformed rate limit policy")


def is_allowed(user_id: str, route: str, limit: int, window: int) -> RateLimitCheckResponse:
    r = redis_client.get_client()
    redis_key = f"ratelimit:{route}:{user_id}"

    current = r.get(redis_key)

    if current is None:
        r.set(redis_key, 1, ex=window)
        return RateLimitCheckResponse(
            allowed=True,
            remaining=limit - 1,
            reset_in=window
        )

    current = int(current)
    ttl = r.ttl(redis_key)

    if current >= limit:
        return RateLimitCheckResponse(
            allowed=False,
            reason="Rate limit exceeded",
            reset_in=ttl
        )

    r.incr(redis_key)
    return RateLimitCheckResponse(
        allowed=True,
        remaining=limit - current - 1,
        reset_in=ttl
    )
