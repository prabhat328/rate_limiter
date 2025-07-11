from pydantic import BaseModel
from typing import Optional


class RateLimitCheckRequest(BaseModel):
    user_id: str
    route_key: str
    role: Optional[str] = None


class RateLimitCheckResponse(BaseModel):
    allowed: bool
    remaining: Optional[int] = None
    reset_in: Optional[int] = None
    reason: Optional[str] = None