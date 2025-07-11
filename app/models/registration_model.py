from pydantic import BaseModel

class UserRegisterRequest(BaseModel):
    name: str

class UserRegisterResponse(BaseModel):
    api_key: str