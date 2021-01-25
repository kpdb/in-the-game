from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from in_the_game.db import metadata

user_profiles = Table(
    "user_profiles",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("user_id", BigInteger, ForeignKey("users.id"), unique=True),
    Column("is_active", Boolean, default=False),
    Column("firstname", String),
    Column("lastname", String),
    Column("country_code", String, nullable=False),
    Column("has_weekly_notifications", Boolean, default=False),
    Column("has_daily_notifications", Boolean, default=False),
    Column("has_live_notifications", Boolean, default=False),
    Column("notification_email", String, nullable=True),
    Column("notification_url", String, nullable=True),
)