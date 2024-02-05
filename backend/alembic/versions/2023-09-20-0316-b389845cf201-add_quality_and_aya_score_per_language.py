"""add_quality_and_aya_score_per_language

Revision ID: b389845cf201
Revises: a7ea807723e4
Create Date: 2023-09-20 03:16:16.357096+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b389845cf201'
down_revision = 'a7ea807723e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add quality_score column to language leaderboard table
    op.add_column(
        "leaderboard_by_language",
        sa.Column(
            "quality_score",
            sa.DECIMAL,
            nullable=True,
        ),
    )

    # add blended rank and blended points to the language leaderboard table
    # as integers
    op.add_column(
        'leaderboard_by_language', 
        sa.Column('blended_rank', 
            sa.Integer(), 
            nullable=True,
        ),
    )
    op.add_column(
        'leaderboard_by_language', 
        sa.Column(
            'blended_points',
            sa.Integer(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    # remove quality_score column from language leaderboard table
    op.drop_column(
        "leaderboard_by_language",
        "quality_score",
    )

    op.drop_column('leaderboard_by_language', 'blended_rank')
    op.drop_column('leaderboard_by_language', 'blended_points')
