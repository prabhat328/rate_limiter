from fastapi import APIRouter, Depends
from typing import List
from app.core.registration import register_user
from app.core.auth import get_api_key
from app.core.policy import save_policy, get_policies, delete_policy
from app.models.registration_model import UserRegisterRequest, UserRegisterResponse
from app.models.policy_model import RateLimitPolicy, RateLimitPolicyResponse, DeletePolicyRequest

router = APIRouter()


@router.post("/register", response_model=UserRegisterResponse)
def register(payload: UserRegisterRequest):
    api_key = register_user(payload.name)
    return {"api_key": api_key}


@router.post("/policy")
def create_policy(
    payload: RateLimitPolicy,
    api_key: str = Depends(get_api_key)
):
    return save_policy(api_key, payload)


@router.get("/policy", response_model=List[RateLimitPolicyResponse])
def fetch_policies(api_key: str = Depends(get_api_key)):
    return get_policies(api_key)


@router.delete("/policy")
def remove_policy(
    payload: DeletePolicyRequest,
    api_key: str = Depends(get_api_key)
):
    return delete_policy(api_key, payload)