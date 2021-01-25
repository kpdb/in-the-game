from in_the_game.db import database
from in_the_game.users.db import user_profiles


async def get_user_profile(user_id):
    query = user_profiles.select().where(user_profiles.c.user_id == user_id)
    return await database.fetch_one(query=query)
