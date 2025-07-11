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

app = FastAPI(
    title="Rate Limiter",
    description="A production-ready API rate limiting service using FastAPI, Redis, and API key management.",
    version="1.0.0",
    contact={
        "name": "Prabhat Tiwari",
        "url": "https://www.linkedin.com/in/prabhat328",
        "email": "prabhat328@outlook.com" 
    },
    lifespan=lifespan
)

app.include_router(router)
