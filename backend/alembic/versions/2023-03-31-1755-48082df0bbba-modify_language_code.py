"""modify_language_code

Revision ID: 48082df0bbba
Revises: 8518c1ce4ee0
Create Date: 2023-03-31 17:55:13.258231+00:00

"""
from alembic import op
import pycountry
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '48082df0bbba'
down_revision = '8518c1ce4ee0'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("ALTER TABLE language_code ALTER COLUMN code TYPE VARCHAR(3)")

    # drop the unique constraint on the code and name columns individually
    op.drop_constraint('language_code_code_key', 'language_code', type_='unique')
    op.drop_constraint('language_code_name_key', 'language_code', type_='unique')

    # add character_code column for characters like 'Latn' or 'Cyrl'
    op.add_column(
        'language_code', 
        sa.Column(
            'character_code', 
            sa.VARCHAR(5), 
            nullable=False,
        )
    )


def downgrade() -> None:
    op.execute("ALTER TABLE language_code ALTER COLUMN code TYPE VARCHAR(2)")
    op.drop_column('language_code', 'character_code')
    op.create_unique_constraint('language_code_code_key', 'language_code', ['code'])
    op.create_unique_constraint('language_code_name_key', 'language_code', ['name'])

