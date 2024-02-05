"""modify_leaderboard_constraints

Revision ID: ff37ca6a9336
Revises: dbde0b456746
Create Date: 2023-05-14 23:55:25.717988+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff37ca6a9336'
down_revision = 'dbde0b456746'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create a unique constraint on username and day for leaderboard_daily
    op.create_unique_constraint(
        'uq_leaderboard_daily_username_day',
        'leaderboard_daily',
        ['username', 'day'],
    )

    # create a unique constraint on username and week for leaderboard_weekly
    op.create_unique_constraint(
        'uq_leaderboard_weekly_username_week',
        'leaderboard_weekly',
        ['username', 'week_of'],
    )

    # create a unique constraint on username and language for leaderboard_by_language
    op.create_unique_constraint(
        'uq_leaderboard_by_language_username_language',
        'leaderboard_by_language',
        ['username', 'language'],
    )

    # create a unique constraint on username for leaderboard_overall
    op.create_unique_constraint(
        'uq_leaderboard_overall_username',
        'leaderboard_overall',
        ['username'],
    )


def downgrade() -> None:
    # drop the unique constraint on username and day for leaderboard_daily
    op.drop_constraint(
        'uq_leaderboard_daily_username_day',
        'leaderboard_daily',
        type_='unique',
    )

    # drop the unique constraint on username and week for leaderboard_weekly
    op.drop_constraint(
        'uq_leaderboard_weekly_username_week',
        'leaderboard_weekly',
        type_='unique',
    )

    # drop the unique constraint on username and language for leaderboard_by_language
    op.drop_constraint(
        'uq_leaderboard_by_language_username_language',
        'leaderboard_by_language',
        type_='unique',
    )

    # drop the unique constraint on username for leaderboard_overall
    op.drop_constraint(
        'uq_leaderboard_overall_username',
        'leaderboard_overall',
        type_='unique',
    )
