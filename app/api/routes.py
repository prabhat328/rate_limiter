from fastapi import APIRouter, Depends
from typing import List
from app.core.registration import register_user
from app.core.auth import get_api_key
from app.core.policy import save_policy, get_policies, delete_policy
from app.core.limiter import get_policy_for, is_allowed
from app.models.request_model import RateLimitCheckRequest, RateLimitCheckResponse
from app.models.registration_model import UserRegisterRequest, UserRegisterResponse
from app.models.policy_model import RateLimitPolicy, RateLimitPolicyResponse, DeletePolicyRequest

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    tags=["User"],
    summary="Register a new application",
    description="Registers a new app owner and returns a unique API key for managing rate limits."
)
def register(payload: UserRegisterRequest):
    api_key = register_user(payload.name)
    return {"api_key": api_key}


@router.post(
    "/policy",
    tags=["Policy"],
    summary="Create or overwrite a rate limit policy",
    description="Define or update a rate limit policy for a specific route and optional role."
)
def create_policy(
    payload: RateLimitPolicy,
    api_key: str = Depends(get_api_key)
):
    return save_policy(api_key, payload)


@router.get(
    "/policy",
    response_model=List[RateLimitPolicyResponse],
    tags=["Policy"],
    summary="Fetch all policies",
    description="Returns all rate limit policies associated with the provided API key."
)
def fetch_policies(api_key: str = Depends(get_api_key)):
    return get_policies(api_key)


@router.delete(
    "/policy",
    tags=["Policy"],
    summary="Delete a specific rate limit policy",
    description="Deletes the rate limit policy for a given route and optional role."
)
def remove_policy(
    payload: DeletePolicyRequest,
    api_key: str = Depends(get_api_key)
):
    return delete_policy(api_key, payload)


@router.post(
    "/check",
    response_model=RateLimitCheckResponse,
    tags=["Rate Limit"],
    summary="Check if a request is allowed",
    description="Validates whether a request is within the defined rate limit for the given user and route."
)
def check_limit(
    payload: RateLimitCheckRequest,
    api_key: str = Depends(get_api_key)
):
    policy = get_policy_for(
        api_key=api_key,
        route_key=payload.route_key,
        role=payload.role
    )

    if not policy["is_active"]:
        return RateLimitCheckResponse(
            allowed=True,
            reason="Rate limiting disabled for this policy"
        )

    return is_allowed(
        user_id=payload.user_id,
        route=payload.route_key,
        limit=policy["limit"],
        window=policy["window_seconds"]
    )