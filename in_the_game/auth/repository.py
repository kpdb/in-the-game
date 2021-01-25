
from in_the_game.db import database
from in_the_game.auth.db import users


async def get_user_by_email(user_email):
    query = users.select().where(users.c.email == user_email)
    return await database.fetch_one(query=query)
