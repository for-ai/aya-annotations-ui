"""add_leaderboard_columns

Revision ID: dbde0b456746
Revises: e10691cae9e3
Create Date: 2023-05-09 21:58:26.091588+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbde0b456746'
down_revision = 'e10691cae9e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add the rank and image_url columns to the leaderboard tables
    op.add_column('leaderboard_daily', sa.Column('rank', sa.Integer(), nullable=True))
    op.add_column('leaderboard_daily', sa.Column('image_url', sa.Text(), nullable=True))

    op.add_column('leaderboard_weekly', sa.Column('rank', sa.Integer(), nullable=True))
    op.add_column('leaderboard_weekly', sa.Column('image_url', sa.Text(), nullable=True))

    op.add_column('leaderboard_by_language', sa.Column('rank', sa.Integer(), nullable=True))
    op.add_column('leaderboard_by_language', sa.Column('image_url', sa.Text(), nullable=True))

    op.add_column('leaderboard_overall', sa.Column('rank', sa.Integer(), nullable=True))    
    op.add_column('leaderboard_overall', sa.Column('image_url', sa.Text(), nullable=True))

def downgrade() -> None:
    # remove the rank and image_url columns from the leaderboard tables
    op.drop_column('leaderboard_daily', 'rank')
    op.drop_column('leaderboard_daily', 'image_url')

    op.drop_column('leaderboard_weekly', 'rank')
    op.drop_column('leaderboard_weekly', 'image_url')

    op.drop_column('leaderboard_by_language', 'rank')
    op.drop_column('leaderboard_by_language', 'image_url')

    op.drop_column('leaderboard_overall', 'rank')
    op.drop_column('leaderboard_overall', 'image_url')
