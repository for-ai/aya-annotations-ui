"""add_quality_score_overall_leaderboard

Revision ID: 8f4f6a9c6a31
Revises: 036364ef81bd
Create Date: 2023-08-07 18:10:02.646046+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f4f6a9c6a31'
down_revision = '036364ef81bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add quality_score column to overall leaderboard table
    op.add_column(
        "leaderboard_overall",
        sa.Column(
            "quality_score",
            sa.DECIMAL,
            nullable=True,
        ),
    )


def downgrade() -> None:
    # remove quality_score column from overall leaderboard table
    op.drop_column(
        "leaderboard_overall",
        "quality_score",
    )
