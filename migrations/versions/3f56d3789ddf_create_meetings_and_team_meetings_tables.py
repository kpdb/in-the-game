"""Create meetings and team_meetings tables

Revision ID: 3f56d3789ddf
Revises: 212b30d96691
Create Date: 2021-01-24 22:27:57.461506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f56d3789ddf'
down_revision = '212b30d96691'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "meetings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("description", sa.String),
        sa.Column("start_time", sa.DateTime),
        sa.Column("end_time", sa.DateTime, nullable=True),
    )

    op.create_table(
        "team_meetings",
        sa.Column("team_id", sa.Integer, sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("meeting_id", sa.Integer, sa.ForeignKey("meetings.id"), nullable=False),
        sa.UniqueConstraint("team_id", "meeting_id", name="unique_team_meeting")
    )


def downgrade():
    op.drop_table("team_meetings")
    op.drop_table("meetings")
