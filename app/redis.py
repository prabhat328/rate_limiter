import redis
from app.config import REDIS_HOST, REDIS_PORT

class RedisClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None

    def connect(self):
        try:
            self.client = redis.Redis(host=self.host, port=self.port, decode_responses=True)
            self.client.ping()
            print("Redis connected.")
        except redis.ConnectionError as e:
            print("Redis connection failed.")
            raise e

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Redis connection closed.")

    def get_client(self):
        if not self.client:
            raise RuntimeError("Redis client not initialized.")
        return self.client


redis_client = RedisClient(REDIS_HOST, REDIS_PORT)
