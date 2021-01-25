from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)

from in_the_game.db import metadata
from in_the_game.teams.models import EventType

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

meeting_events = Table(
    "meeting_events",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("description", String),
    Column("occured_at", DateTime),
    Column("type", Enum(EventType)),
    Column("meeting_id", Integer, ForeignKey("meetings.id")),
)
