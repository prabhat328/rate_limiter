from fastapi import Header, HTTPException
from redis.exceptions import RedisError
from app.redis import redis_client

def get_api_key(x_api_key: str = Header(...)):
    try:
        r = redis_client.get_client()
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    if not r.exists(f"user:{x_api_key}"):
        raise HTTPException(status_code=401, detail="Invalid API key")

    return x_api_key
