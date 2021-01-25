from sqlalchemy import and_
from in_the_game.db import database
from in_the_game.users.db import user_profiles, subscribed_teams
from in_the_game.users.models import Profile


async def get_user_profile(user_id: int):
    query = user_profiles.select().where(user_profiles.c.user_id == user_id)
    return await database.fetch_one(query=query)


async def update_user_profile(user_id: int, new_profile: Profile):
    query = (
        user_profiles
        .update()
        .where(user_profiles.c.user_id == user_id)
        .values(
            firstname=new_profile.firstname,
            lastname=new_profile.lastname,
            country_code=new_profile.country_code,
            has_weekly_notifications=new_profile.has_weekly_notifications,
            has_daily_notifications=new_profile.has_daily_notifications,
            has_live_notifications=new_profile.has_live_notifications,
            notification_url=new_profile.notification_url,
            notification_email=new_profile.notification_email,
        )
        .returning(user_profiles)
    )
    return await database.execute(query=query)


async def get_user_subscriptions(user_profile_id: int):
    query = (
        subscribed_teams
        .select()
        .where(subscribed_teams.c.user_profile_id == user_profile_id)
    )
    return await database.fetch_all(query=query)


async def create_user_subscription(user_profile_id: int, team_id: int):
    query = subscribed_teams.insert(user_profile_id=user_profile_id, team_id=team_id)
    return await database.execute(query=query)


async def delete_user_subscription(user_profile_id: int, team_id: int):
    query = subscribed_teams.delete().where(
        and_(
            subscribed_teams.c.user_profile_id == user_profile_id,
            subscribed_teams.c.team_id == team_id,
        )
    )
    return await database.execute(query=query)
