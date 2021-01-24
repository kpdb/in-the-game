from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint

from in_the_game.db import metadata


teams = Table(
    "teams",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("description", String),
    Column("country_code", String),
    Column("group", String),
    Column("organization", String),
)

meetings = Table(
    "meetings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("description", String),
    Column("start_time", DateTime),
    Column("end_time", DateTime, nullable=True),
)

team_meetings = Table(
    "team_meetings",
    metadata,
    Column("team_id", Integer, ForeignKey("teams.id"), nullable=False),
    Column("meeting_id", Integer, ForeignKey("meetings.id"), nullable=False),
    UniqueConstraint("team_id", "meeting_id", name="unique_team_meeting")
)
