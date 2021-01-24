
from typing import List
from in_the_game.db import database
from in_the_game.teams.models import NewTeam, NewMeeting
from in_the_game.teams.db import teams, meetings, team_meetings


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


async def assign_team_to_meeting(meeting_id: int, team_id: int):
    query = team_meetings.insert(meeting_id=meeting_id, team_id=team_id)
    return await database.execute(query=query)
