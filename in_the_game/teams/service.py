from typing import List
from .models import NewTeam, Team, NewMeeting, Meeting, NewMeetingEvent, MeetingEvent
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


async def get_meeting(meeting_id: int) -> Meeting:
    meeting_data = await repository.get_meeting(meeting_id)
    meeting_events = await repository.get_meeting_events(meeting_id)
    assigned_teams = await repository.get_meeting_teams(meeting_id)
    return Meeting(
        events=meeting_events,
        teams=assigned_teams,
        **meeting_data,
    )


async def create_meeting_event(new_meeting_event: NewMeetingEvent) -> MeetingEvent:
    meeting_event_id = await repository.create_meeting_event(new_meeting_event)
    return MeetingEvent(
        id=meeting_event_id,
        type=new_meeting_event.type,
        description=new_meeting_event.description,
        occured_at=new_meeting_event.occured_at,
    )
