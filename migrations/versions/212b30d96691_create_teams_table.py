"""Create teams table

Revision ID: 212b30d96691
Revises: 
Create Date: 2021-01-24 18:19:03.344023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "212b30d96691"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("description", sa.String),
        sa.Column("country_code", sa.String),
        sa.Column("group", sa.String),
        sa.Column("organization", sa.String),
    )


def downgrade():
    op.drop_table("teams")
