import time
from fastapi import Request, HTTPException
from app.redis import redis_client

def limit_by_ip(limit: int, window_seconds: int):
    async def limiter(request: Request):
        ip = request.client.host
        key = f"iplimit:{ip}"
        r = redis_client.get_client()

        current = r.get(key)
        if current is None:
            r.setex(key, window_seconds, 1)
        else:
            count = int(current)
            if count >= limit:
                raise HTTPException(status_code=429, detail="Too many requests from this IP")
            r.incr(key)

    return limiter
