"""Create subscribed_teams table

Revision ID: b965665757fc
Revises: 02c7a8510a2a
Create Date: 2021-01-25 13:17:42.497008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b965665757fc'
down_revision = '02c7a8510a2a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "subscribed_teams",
        sa.Column("user_profile_id", sa.BigInteger, sa.ForeignKey("user_profiles.id")),
        sa.Column("team_id", sa.Integer, sa.ForeignKey("teams.id")),
        sa.UniqueConstraint("user_profile_id", "team_id", name="unique_user_subscriptions"),
    )


def downgrade():
    op.drop_table("subscribed_teams")
