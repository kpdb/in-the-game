from datetime import datetime, timedelta
from arq import create_pool

from in_the_game.broker import settings
from in_the_game.users import service as user_service
from .models import NewMeetingEvent
from . import service

# TODO: kod znajdujący się w tym module nie jest gotowy do uruchomienia. pokazuje raczej
#       zarys logiki, którą będą uruchamiać poszczególne zadania.

async def initialize_weekly_notifications(ctx):
    print("weekly notification init")
    broker = await create_pool(settings)
    await broker.enqueue_job("create_periodic_notifications", 7)


async def initialize_daily_notifications(ctx):
    print("daily notification init")
    broker = await create_pool(settings)
    await broker.enqueue_job("create_periodic_notifications", 1)


async def create_periodic_notifications(ctx, period_in_days):
    print(f"ho-ho, notification for next {period_in_days} days")
    # get all meetings that has start_time between now and now + period_in_days
    start_time = datetime.now()
    end_time = start_time + timedelta(days=period_in_days)
    current_meetings = service.get_meetings_starting_between(start_time, end_time)

    # get all user_profiles that has_weekly_notifications==True and is_active==True
    profiles_to_notify = user_service.get_user_profiles(has_weekly_notifications=True)
    # create two lists (one for each notification method)
    #  and iterating through user_profiles read and append available emails/urls to
    #  respective lists

    # prepare notification message

    # enqueue prepared content with list of emails for email_notification_handler
    # enqueue prepared content with list of urls for url_notification_handler




async def create_live_notifications(ctx, meeting_id: int, meeting_event: NewMeetingEvent):
    print("this should handle live event's notifications")