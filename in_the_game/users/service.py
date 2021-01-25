from typing import Optional, List
from . import repository
from .models import Profile


async def get_user_profile(user_id: int) -> Optional[Profile]:
    profile_data = await repository.get_user_profile(user_id)
    if profile_data:
        user_subscriptions = await repository.get_user_subscriptions(profile_data['id'])
        subscribed_team_ids = [subscription['team_id'] for subscription in user_subscriptions]
        return Profile(team_ids=subscribed_team_ids, **profile_data)
    return None


async def update_user_profile(user_id: int, new_profile: Profile) -> Optional[Profile]:
    profile_data = await repository.get_user_profile(user_id)
    if profile_data:
        updated_subscriptions = await update_user_subscriptions(profile_data['id'], new_profile.team_ids)
        updated_profile_data = await repository.update_user_profile(user_id, new_profile)
        return Profile(team_ids=updated_subscriptions, **updated_profile_data)
    return None


async def update_user_subscriptions(user_profile_id: int, new_subscriptions: List[int]):
    user_subscriptions = await repository.get_user_subscriptions(user_profile_id)

    subscribed_team_ids = set([subscription['team_id'] for subscription in user_subscriptions])
    updated_team_ids = set(new_subscriptions)

    subscriptions_to_remove = subscribed_team_ids - updated_team_ids
    subscriptions_to_create = updated_team_ids - subscribed_team_ids

    async with repository.database.transaction():
        for team_id in subscriptions_to_remove:
            await repository.delete_user_subscription(user_profile_id, team_id)
        for team_id in subscriptions_to_create:
            await repository.create_user_subscription(user_profile_id, team_id)

    return new_subscriptions
