"""remove_translation_xp3_tasks

Revision ID: c2583aaea36f
Revises: 97c68b55f6b7
Create Date: 2023-07-06 12:48:37.075026+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2583aaea36f'
down_revision = '97c68b55f6b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # deactivate datasets that are from:
    # 'dataset/sample_100/xp3_GEM_wiki_lingua', 'dataset/sample_100/xp3_Helsinki-NLP_tatoeba', 
    # and 'dataset/sample_100/xp3_allenai_wmt22_african'
    op.execute("""
    UPDATE dataset 
    SET active = false 
    WHERE name LIKE '%%dataset/sample_100/xp3_GEM_wiki_lingua%'
    OR name LIKE '%%dataset/sample_100/xp3_Helsinki-NLP_tatoeba%'
    OR name LIKE '%%dataset/sample_100/xp3_allenai_wmt22_african%'
    """)


def downgrade() -> None:
    op.execute("""
    UPDATE dataset
    SET active = true
    WHERE name LIKE '%%dataset/sample_100/xp3_GEM_wiki_lingua%'
    OR name LIKE '%%dataset/sample_100/xp3_Helsinki-NLP_tatoeba%'
    OR name LIKE '%%dataset/sample_100/xp3_allenai_wmt22_african%'
    """)
