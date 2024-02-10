"""fix_panjabi_direction

Revision ID: 9fdf109afc92
Revises: aec96b6f1dd6
Create Date: 2023-07-05 18:57:30.311661+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fdf109afc92'
down_revision = 'aec96b6f1dd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # make sure Panjabi is ltr and not rtl
    op.execute("UPDATE language_code SET direction = 'ltr' WHERE code = 'pan';")


def downgrade() -> None:
    # make sure Panjabi is rtl and not ltr
    op.execute("UPDATE language_code SET direction = 'rtl' WHERE code = 'pan';")
