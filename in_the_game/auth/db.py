from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    String,
    Table,
)
from in_the_game.db import metadata

users = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("email", String, unique=True),
    Column("password", String),
    Column("created_at", DateTime, nullable=False),
    Column("modified_at", DateTime),
)
