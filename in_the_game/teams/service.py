from typing import List
from .models import NewTeam, Team, NewMeeting, Meeting
from . import repository


async def create_team(new_team: NewTeam) -> Team:
    team_id = await repository.create_team(new_team)

    return Team(
        id=team_id,
        **new_team.dict()
    )


async def get_all_teams() -> List[Team]:
    result = await repository.get_all_teams()

    return [
        Team(**team_data)
        for team_data in result
    ]


async def create_meeting(new_meeting: NewMeeting) -> Meeting:
    async with repository.database.transaction():
        assigned_teams = await repository.get_all_teams_with_ids(new_meeting.team_ids)
        meeting_id = await repository.create_meeting(new_meeting)
        for team_id in new_meeting.team_ids:
            await repository.assign_team_to_meeting(meeting_id, team_id)

    return Meeting(
        id=meeting_id,
        description=new_meeting.description,
        start_time=new_meeting.start_time,
        end_time=new_meeting.end_time,
        teams=assigned_teams,
    )
