"""add_fields_to_leaderboards

Revision ID: f233a368f1c4
Revises: ff37ca6a9336
Create Date: 2023-05-15 01:34:00.478188+00:00

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'f233a368f1c4'
down_revision = 'ff37ca6a9336'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add the user_id column to leaderboard_daily, leaderboard_weekly, leaderboard_by_language, and leaderboard_overall
    op.add_column(
        'leaderboard_daily',
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
    )
    op.add_column(
        'leaderboard_weekly',
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
    )
    op.add_column(
        'leaderboard_by_language',
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
    )
    op.add_column(
        'leaderboard_overall',
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
    )

    # add the language_code column to leaderboard_by_language
    op.add_column(
        'leaderboard_by_language',
        sa.Column('language_code', sa.String(), nullable=False),
    )


def downgrade() -> None:
    # drop the user_id column from leaderboard_daily, leaderboard_weekly, leaderboard_by_language, and leaderboard_overall
    op.drop_column('leaderboard_daily', 'user_id')
    op.drop_column('leaderboard_weekly', 'user_id')
    op.drop_column('leaderboard_by_language', 'user_id')
    op.drop_column('leaderboard_overall', 'user_id')

    # drop the language_code column from leaderboard_by_language
    op.drop_column('leaderboard_by_language', 'language_code')
