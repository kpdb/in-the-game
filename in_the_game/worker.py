from arq import cron

from in_the_game.broker import settings
from in_the_game.db import database
from in_the_game.teams import tasks as team_tasks
from in_the_game.notifications import tasks as notification_tasks


async def startup(ctx):
    await database.connect()


async def shutdown(ctx):
    await database.disconnect()


class WorkerSettings:
    redis_settings = settings
    on_startup = startup
    on_shutdown = shutdown
    cron_jobs = [
        cron(team_tasks.initialize_weekly_notifications, weekday='mon', hour=6, minute=5),
        cron(team_tasks.initialize_daily_notifications, weekday={0, 1, 2, 3, 4}, hour=6, minute=5),
    ]
    functions = [
        team_tasks.create_periodic_notifications,
        team_tasks.create_live_notifications,
        notification_tasks.send_url_notifications,
        notification_tasks.send_email_notifications,
    ]
