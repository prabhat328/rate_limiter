import time
from app.redis import redis_client
from app.utils.API_generator import generate_api_key

def register_user(name: str) -> str:
    r = redis_client.get_client()

    api_key = generate_api_key()
    user_key = f"user:{api_key}"

    # Ensure key doesn’t already exist
    while r.exists(user_key):
        api_key = generate_api_key()
        user_key = f"user:{api_key}"

    user_data = {
        "name": name,
        "created_at": str(int(time.time()))
    }

    r.hset(user_key, mapping=user_data)

    return api_key
