from fastapi import APIRouter, Body

from . import service
from .models import Profile

router = APIRouter()


@router.get("/{user_id}/profile", response_model=Profile)
async def get_user_profile(user_id: int):
    return await service.get_user_profile(user_id)


@router.put("/{user_id}/profile", response_model=Profile)
async def update_user_profile(user_id: int, profile: Profile = Body(...)):
    return await service.update_user_profile(user_id, profile)
