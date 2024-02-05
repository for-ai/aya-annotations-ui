"""deactivate_gem_wiki_sum_datasets

Revision ID: 53f48b99dd8c
Revises: 68daab0b8ccb
Create Date: 2023-06-19 11:54:11.693539+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53f48b99dd8c'
down_revision = '68daab0b8ccb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # update the datasets table to make the gem_wiki_cat_sum datasets inactive
    op.execute(
        """
        UPDATE dataset
        SET active = false
        WHERE name LIKE '%GEM_wiki_cat_sum%';
        """
    )


def downgrade() -> None:
    # update the datasets table to make the gem_wiki_cat_sum datasets active
    op.execute(
        """
        UPDATE dataset
        SET active = true
        WHERE name LIKE '%GEM_wiki_cat_sum%';
        """
    )
