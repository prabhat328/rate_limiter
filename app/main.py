from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router
from app.redis import redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before app starts
    redis_client.connect()
    yield
    # On shutdown
    redis_client.disconnect()

app = FastAPI(title="Rate Limiter", lifespan=lifespan)
app.include_router(router)
