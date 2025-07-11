from pydantic import BaseModel, Field
from typing import Optional

class RateLimitPolicy(BaseModel):
    route_key: str = Field(..., example="get_user")
    limit: int = Field(..., gt=0, lt=100, example=10)
    window_seconds: int = Field(..., gt=0, lt=60, example=20)
    description: Optional[str] = Field(None, example="Limit for get_user endpoint")
    is_active: bool = Field(default=True)
    role: Optional[str] = Field(None, example="admin")


class RateLimitPolicyResponse(BaseModel):
    route_key: str
    limit: int
    window_seconds: int
    is_active: bool
    role: Optional[str]
    description: Optional[str]

class DeletePolicyRequest(BaseModel):
    route_key: str
    role: Optional[str] = None