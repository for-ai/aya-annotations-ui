
"""rename_pedi_to_northern_sotho

Revision ID: 35875912fb74
Revises: 233490849236
Create Date: 2023-07-01 12:50:02.278126+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35875912fb74'
down_revision = '233490849236'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE language_code SET name = 'Northern Sotho' WHERE code = 'nso'")


def downgrade() -> None:
    op.execute("UPDATE language_code SET name = 'Pedi' WHERE code = 'nso'")
