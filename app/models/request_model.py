from pydantic import BaseModel

class RateLimitRequest(BaseModel):
    user_id: str
    route_key: str
    limit: int
    window_seconds: int

class RateLimitResponse(BaseModel):
    allowed: bool
    remaining: int
    reset_in: int