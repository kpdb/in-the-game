
from typing import List
from in_the_game.db import database
from in_the_game.teams.models import NewTeam, NewMeeting, NewMeetingEvent
from in_the_game.teams.db import teams, meetings, team_meetings, meeting_events


async def create_team(payload: NewTeam):
    query = teams.insert().values(
        name=payload.name,
        description=payload.description,
        country_code=payload.country_code,
        group=payload.group,
        organization=payload.organization,
    )
    return await database.execute(query=query)


async def get_all_teams():
    query = teams.select()
    return await database.fetch_all(query=query)


async def get_all_teams_with_ids(team_ids: List[int]):
    query = teams.select().where(teams.c.id.in_(team_ids))
    return await database.fetch_all(query=query)


async def create_meeting(payload: NewMeeting):
    query = meetings.insert().values(
        description=payload.description,
        start_time=payload.start_time,
        end_time=payload.end_time,
    )

    return await database.execute(query=query)


async def get_meeting(meeting_id: int):
    query = meetings.select().where(meetings.c.id == meeting_id)
    return await database.fetch_one(query=query)


async def assign_team_to_meeting(meeting_id: int, team_id: int):
    query = team_meetings.insert(meeting_id=meeting_id, team_id=team_id)
    return await database.execute(query=query)


async def get_meeting_teams(meeting_id: int):
    query = teams.select().select_from(
        teams.join(team_meetings, team_meetings.c.meeting_id == meeting_id)
    )
    return await database.execute(query=query)


async def get_team_meetings(team_id: int):
    query = meetings.select().select_from(
        meetings.join(team_meetings, team_meetings.c.team_id == team_id)
    )
    return await database.execute(query=query)


async def create_meeting_event(payload: NewMeetingEvent):
    query = meeting_events.insert(
        type=payload.type,
        description=payload.description,
        occured_at=payload.occured_at,
        meeting_id=payload.meeting_id,
    )
    return await database.execute(query=query)


async def get_meeting_events(meeting_id: int):
    query = meeting_events.select().where(meeting_events.c.meeting_id == meeting_id)
    return await database.fetch_all(query=query)
