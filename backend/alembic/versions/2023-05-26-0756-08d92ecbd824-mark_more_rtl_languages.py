"""mark_more_rtl_languages

Revision ID: 08d92ecbd824
Revises: 7e4985d7daa7
Create Date: 2023-05-26 07:56:16.568111+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08d92ecbd824'
down_revision = '7e4985d7daa7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # mark the following languages as RTL:
    # Pashto, Panjabi, Iranian Persian
    op.execute(
        """
        UPDATE language_code
        SET direction = 'rtl'
        WHERE code IN ('pes', 'pan', 'pbt');
        """
    )



def downgrade() -> None:
    # mark the following languages as LTR:
    # Pashto, Panjabi, Iranian Persian
    op.execute(
        """
        UPDATE language_code
        SET direction = 'ltr'
        WHERE code IN ('pes', 'pan', 'pbt');
        """
    )
