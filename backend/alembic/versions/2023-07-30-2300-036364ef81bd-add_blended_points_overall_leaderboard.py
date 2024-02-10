"""add_blended_points_overall_leaderboard

Revision ID: 036364ef81bd
Revises: 5c6ab0fe5920
Create Date: 2023-07-30 23:00:50.251212+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '036364ef81bd'
down_revision = '5c6ab0fe5920'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add blended rank and blended points to the overall leaderboard table
    # as integers
    op.add_column('leaderboard_overall', sa.Column('blended_rank', sa.Integer(), nullable=True))
    op.add_column('leaderboard_overall', sa.Column('blended_points', sa.Integer(), nullable=True))

def downgrade() -> None:
    # remove blended rank and blended points from the overall leaderboard table
    op.drop_column('leaderboard_overall', 'blended_rank')
    op.drop_column('leaderboard_overall', 'blended_points')
