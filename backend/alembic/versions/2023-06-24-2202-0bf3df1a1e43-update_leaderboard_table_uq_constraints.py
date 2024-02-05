"""update_leaderboard_table_uq_constraints

Revision ID: 0bf3df1a1e43
Revises: b9d22315640b
Create Date: 2023-06-24 22:02:07.372951+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bf3df1a1e43'
down_revision = 'b9d22315640b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # the leaderboard tables should have a unique constraint on the user_id column
    # rather than the username column, since users can change their username
    # and we don't want to have to manually fix data in the leaderboard table every time
    # a user changes their username

    # drop the current constraints on username and day for leaderboard_daily
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

    # create a unique constraint on user_id and day for leaderboard_daily
    op.create_unique_constraint(
        'uq_leaderboard_daily_user_id_day',
        'leaderboard_daily',
        ['user_id', 'day'],
    )

    # create a unique constraint on user_id and week for leaderboard_weekly
    op.create_unique_constraint(
        'uq_leaderboard_weekly_user_id_week',
        'leaderboard_weekly',
        ['user_id', 'week_of'],
    )

    # create a unique constraint on user_id and language for leaderboard_by_language
    op.create_unique_constraint(
        'uq_leaderboard_by_language_user_id_language',
        'leaderboard_by_language',
        ['user_id', 'language'],
    )

    # create a unique constraint on user_id for leaderboard_overall
    op.create_unique_constraint(
        'uq_leaderboard_overall_user_id',
        'leaderboard_overall',
        ['user_id'],
    )



def downgrade() -> None:
    # do the inverse of the above operations

    # drop the current constraints on user_id and day for leaderboard_daily
    op.drop_constraint(
        'uq_leaderboard_daily_user_id_day',
        'leaderboard_daily',
        type_='unique',
    )

    # drop the unique constraint on user_id and week for leaderboard_weekly
    op.drop_constraint(
        'uq_leaderboard_weekly_user_id_week',
        'leaderboard_weekly',
        type_='unique',
    )

    # drop the unique constraint on user_id and language for leaderboard_by_language
    op.drop_constraint(
        'uq_leaderboard_by_language_user_id_language',
        'leaderboard_by_language',
        type_='unique',
    )

    # drop the unique constraint on user_id for leaderboard_overall
    op.drop_constraint(
        'uq_leaderboard_overall_user_id',
        'leaderboard_overall',
        type_='unique',
    )


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
