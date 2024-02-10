"""add_user_languages_to_leaderboards

Revision ID: 38bb36535ede
Revises: cf118e4d101b
Create Date: 2023-06-02 04:01:21.383819+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38bb36535ede'
down_revision = 'cf118e4d101b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add a `languages` column to the leaderboard_daily table
    # repeat for weekly and overall. it should be an array of text
    op.add_column(
        "leaderboard_daily",
        sa.Column(
            "languages",
            sa.ARRAY(sa.Text),
            # NOTE: this is nullable temporarily while we don't 
            # have to backfill leaderboard data yet
            nullable=True,
        ),
    )

    op.add_column(
        "leaderboard_weekly",
        sa.Column(
            "languages",
            sa.ARRAY(sa.Text),
            nullable=True,
        ),
    )

    op.add_column(
        "leaderboard_overall",
        sa.Column(
            "languages",
            sa.ARRAY(sa.Text),
            nullable=True,
        ),
    )
    

def downgrade() -> None:
    # remove the `languages` column from the leaderboard_daily table
    # repeat for weekly and overall.
    op.drop_column("leaderboard_daily", "languages")
    op.drop_column("leaderboard_weekly", "languages")
    op.drop_column("leaderboard_overall", "languages")
