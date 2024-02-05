"""add_iban_language

Revision ID: 2ba53ea38f6c
Revises: 476d8e005a09
Create Date: 2023-08-30 23:10:59.505238+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ba53ea38f6c'
down_revision = '476d8e005a09'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add Iban as a language, for task 2 support
    # https://iso639-3.sil.org/code/iba
    op.execute(
        """
        INSERT INTO language_code (code, name, character_code, direction)
        VALUES ('iba', 'Iban', 'Latn', 'ltr');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM language_code
        WHERE code = 'iba';
        """
    )
