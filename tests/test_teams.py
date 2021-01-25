from contextlib import asynccontextmanager
from datetime import datetime

import pytest
from in_the_game.teams import models, repository, service


def test_get_all_teams(test_app, monkeypatch):
    test_response_data = [
        {
            "id": 1,
            "name": "a",
            "description": "aa",
            "country_code": "pl",
            "group": "aaa",
            "organization": "aaaa",
        },
        {
            "id": 2,
            "name": "b",
            "description": "bb",
            "country_code": "pl",
            "group": "bbb",
            "organization": "bbbb",
        },
    ]

    async def mock_get_all_teams():
        return test_response_data

    monkeypatch.setattr(repository, "get_all_teams", mock_get_all_teams)

    response = test_app.get("/teams")
    assert response.status_code == 200
    assert response.json() == test_response_data


@pytest.mark.asyncio
async def test_create_team(test_app, monkeypatch):
    test_team = models.NewTeam(
        name='Best team',
        description='name says it all',
        country_code='PL',
        group='Extraklasa',
        organization='PZPN',
    )

    async def mock_create_team(payload):
        return 1

    monkeypatch.setattr(repository, "create_team", mock_create_team)

    created_team = await service.create_team(test_team)
    assert created_team.id == 1
    assert created_team.name == test_team.name


@pytest.mark.asyncio
async def test_create_team_without_optional_values(test_app, monkeypatch):
    test_team = models.NewTeam(
        name='Best team',
        description='name says it all',
        country_code='PL',
    )

    async def mock_create_team(payload):
        return 1

    monkeypatch.setattr(repository, "create_team", mock_create_team)

    created_team = await service.create_team(test_team)
    assert created_team.id == 1
    assert created_team.name == test_team.name
    assert created_team.group is None
    assert created_team.organization is None


@pytest.mark.asyncio
async def test_create_meeting(monkeypatch):
    test_meeting = models.NewMeeting(
        description="a",
        start_time=datetime.now(),
        end_time=datetime.now(),
        team_ids=[1, 2, 3],
    )

    @asynccontextmanager
    async def mock_db_transaction():
        yield None

    async def mock_create_meeting(payload):
        return 1

    async def mock_assign_team_to_meeting(meeting_id, team_id):
        return team_id

    async def mock_get_all_teams_with_ids(team_ids):
        return [
            {
                "id": team_id,
                "name": f"Name_{team_id}",
                "description": f"Description_{team_id}",
                "country_code": "pl",
                "group": "a",
                "organization": "b",
            }
            for team_id in team_ids
        ]

    monkeypatch.setattr(repository, "create_meeting", mock_create_meeting)
    monkeypatch.setattr(repository, "assign_team_to_meeting", mock_assign_team_to_meeting)
    monkeypatch.setattr(repository, "get_all_teams_with_ids", mock_get_all_teams_with_ids)
    monkeypatch.setattr(repository.database, "transaction", mock_db_transaction)

    created_meeting = await service.create_meeting(test_meeting)
    assert created_meeting.id == 1


@pytest.mark.asyncio
async def test_get_meeting(monkeypatch):
    test_meeting_data = {
        "id": 1,
        "description": "a",
        "start_time": datetime.now(),
        "end_time": datetime.now(),
    }

    async def mock_get_meeting(meeting_id):
        return test_meeting_data

    async def mock_get_meeting_teams(meeting_id):
        return [
            {
                "id": team_id,
                "name": f"Name_{team_id}",
                "description": f"Description_{team_id}",
                "country_code": "pl",
                "group": "a",
                "organization": "b",
            }
            for team_id in [1, 2, 3]
        ]

    async def mock_get_meeting_events(meeting_id):
        return [
            {
                "id": event_id,
                "type": "meeting_start",
                "description": f"Description_{event_id}",
                "occured_at": datetime.now(),
                "meeting_id": meeting_id,
            }
            for event_id in [4, 5, 6]
        ]

    monkeypatch.setattr(repository, "get_meeting", mock_get_meeting)
    monkeypatch.setattr(repository, "get_meeting_teams", mock_get_meeting_teams)
    monkeypatch.setattr(repository, "get_meeting_events", mock_get_meeting_events)

    meeting = await service.get_meeting(1)
    assert meeting.id == 1
    assert [team.id for team in meeting.teams] == [1, 2, 3]
    assert [event.id for event in meeting.events] == [4, 5, 6]


@pytest.mark.asyncio
async def test_create_meeting_event(monkeypatch):
    test_event = models.NewMeetingEvent(
        description="a",
        occured_at=datetime.now(),
        type=models.EventType.MEETING_START,
        meeting_id=1,
    )

    async def mock_create_meeting_event(payload):
        return 1

    monkeypatch.setattr(repository, "create_meeting_event", mock_create_meeting_event)

    created_event = await service.create_meeting_event(test_event)
    assert created_event.id == 1
    assert created_event.type == test_event.type
