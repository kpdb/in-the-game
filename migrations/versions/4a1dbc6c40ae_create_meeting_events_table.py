"""Create meeting_events table

Revision ID: 4a1dbc6c40ae
Revises: 3f56d3789ddf
Create Date: 2021-01-25 01:03:02.257274

"""
from alembic import op
import sqlalchemy as sa

from in_the_game.teams.models import EventType


# revision identifiers, used by Alembic.
revision = '4a1dbc6c40ae'
down_revision = '3f56d3789ddf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "meeting_events",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("description", sa.String),
        sa.Column("occured_at", sa.DateTime),
        sa.Column("type", sa.Enum(EventType)),
        sa.Column("meeting_id", sa.Integer, sa.ForeignKey("meetings.id")),
    )


def downgrade():
    op.drop_table("meeting_events")
    op.execute("DROP TYPE eventtype")
