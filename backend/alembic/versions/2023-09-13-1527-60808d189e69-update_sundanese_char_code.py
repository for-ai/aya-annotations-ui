"""update_sundanese_char_code

Revision ID: 60808d189e69
Revises: 2ba53ea38f6c
Create Date: 2023-09-13 15:27:36.704062+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60808d189e69'
down_revision = '2ba53ea38f6c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # set the character_code for sundanese from Arab to Latn
    op.execute("UPDATE language_code SET character_code = 'Latn' WHERE name = 'Sundanese'")


def downgrade() -> None:
    # set the character_code for sundanese from Latn to Arab
    op.execute("UPDATE language_code SET character_code = 'Arab' WHERE name = 'Sundanese'")
