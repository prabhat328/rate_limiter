from pydantic import BaseModel
from typing import Optional

class LogEntry(BaseModel):
    timestamp: int
    user_id: str
    route: str
    role: Optional[str]
    allowed: bool
    reason: Optional[str]
