"""modify_dataset_name_to_text

Revision ID: 8518c1ce4ee0
Revises: cb5b5832ab95
Create Date: 2023-03-31 17:47:52.767578+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8518c1ce4ee0'
down_revision = 'cb5b5832ab95'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE dataset ALTER COLUMN name TYPE TEXT")


def downgrade() -> None:
    op.execute("ALTER TABLE dataset ALTER COLUMN name TYPE VARCHAR(64)")
