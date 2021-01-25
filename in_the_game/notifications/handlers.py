from typing import List
from in_the_game.teams.models import Meeting, NewMeetingEvent


async def create_weekly_notification_content(weekly_meetings: List[Meeting]) -> str:
    return ''


async def create_daily_notification_content(daily_meetings: List[Meeting]) -> str:
    return ''


async def create_live_notification_content(meeting_event: NewMeetingEvent) -> str:
    return ''
