from typing import Optional
from . import repository
from .models import Profile


async def get_user_profile(user_id: int) -> Optional[Profile]:
    profile_data = await repository.get_user_profile(user_id)
    if profile_data:
        return Profile(**profile_data)
    return None
