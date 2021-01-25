"""Create user and user_profile tables

Revision ID: 02c7a8510a2a
Revises: 4a1dbc6c40ae
Create Date: 2021-01-25 09:47:10.762942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02c7a8510a2a'
down_revision = '4a1dbc6c40ae'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("email", sa.String, unique=True),
        sa.Column("password", sa.String),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("modified_at", sa.DateTime),
    )
    op.create_table(
        "user_profiles",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("user_id", sa.BigInteger, sa.ForeignKey("users.id"), unique=True),
        sa.Column("is_active", sa.Boolean, default=False),
        sa.Column("firstname", sa.String),
        sa.Column("lastname", sa.String),
        sa.Column("country_code", sa.String, nullable=False),
        sa.Column("has_weekly_notifications", sa.Boolean, default=False),
        sa.Column("has_daily_notifications", sa.Boolean, default=False),
        sa.Column("has_live_notifications", sa.Boolean, default=False),
        sa.Column("notification_email", sa.String, nullable=True),
        sa.Column("notification_url", sa.String, nullable=True),
    )


def downgrade():
    op.drop_table("user_profiles")
    op.drop_table("users")
