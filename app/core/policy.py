from app.redis import redis_client
from app.models.policy_model import RateLimitPolicy, RateLimitPolicyResponse, DeletePolicyRequest
from typing import Optional, List
from redis.exceptions import RedisError
from fastapi import HTTPException

def save_policy(api_key: str, policy: RateLimitPolicy):
    try:
        r = redis_client.get_client()
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis connection failed")

    try:
        role = policy.role if policy.role else "default"
        redis_key = f"policy:{api_key}:{policy.route_key}:{role}"

        r.hset(redis_key, mapping={
            "limit": policy.limit,
            "window": policy.window_seconds,
            "description": policy.description or "",
            "is_active": str(int(policy.is_active))
        })

        return {"message": "Policy saved successfully."}

    except RedisError:
        raise HTTPException(status_code=503, detail="Failed to write to Redis")

    except Exception:
        raise HTTPException(status_code=500, detail="Unknown error while saving policy")


def get_policies(api_key: str) -> List[RateLimitPolicyResponse]:
    try:
        r = redis_client.get_client()
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    pattern = f"policy:{api_key}:*"
    keys = r.scan_iter(match=pattern)
    policies = []

    for key in keys:
        parts = key.split(":")
        if len(parts) < 4:
            continue  # malformed key

        _, _, route_key, role = parts

        data = r.hgetall(key)
        try:
            policies.append(RateLimitPolicyResponse(
                route_key=route_key,
                role=None if role == "default" else role,
                limit=int(data.get("limit", 0)),
                window_seconds=int(data.get("window", 0)),
                description=data.get("description", ""),
                is_active=bool(int(data.get("is_active", "0")))
            ))
        except Exception:
            continue

    return policies


def delete_policy(api_key: str, payload: DeletePolicyRequest):
    try:
        r = redis_client.get_client()
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    redis_key = f"policy:{api_key}:{payload.route_key}:{payload.role}"
    deleted = r.delete(redis_key)

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Policy not found")

    return {"message": "Policy deleted"}