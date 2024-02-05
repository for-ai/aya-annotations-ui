"""unique_language_code_records

Revision ID: 518a194fa402
Revises: eb13778e0573
Create Date: 2023-04-24 00:59:42.578691+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '518a194fa402'
down_revision = 'eb13778e0573'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ensure that the language_code table has unique records
    op.create_unique_constraint(
        constraint_name="unique_language_code_code_name_character_code",
        table_name="language_code",
        columns=["code", "name", "character_code"],
    )


def downgrade() -> None:
    op.drop_constraint(
        constraint_name="unique_language_code_code_name_character_code",
        table_name="language_code",
    )
