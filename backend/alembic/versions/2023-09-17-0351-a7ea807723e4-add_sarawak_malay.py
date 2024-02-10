"""add_sarawak_malay

Revision ID: a7ea807723e4
Revises: 60808d189e69
Create Date: 2023-09-17 03:51:36.719887+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7ea807723e4'
down_revision = '60808d189e69'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add Sarawak Malay as a language, for task 2 support
    op.execute(
        """
        INSERT INTO language_code (code, name, character_code, direction)
        VALUES ('poz', 'Sarawak Malay', 'Latn', 'ltr');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM language_code
        WHERE code = 'poz';
        """
    )
