"""add_more_languages

Revision ID: 5536f1b704eb
Revises: 518a194fa402
Create Date: 2023-04-28 02:09:42.326327+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5536f1b704eb'
down_revision = '518a194fa402'
branch_labels = None
depends_on = None

# initial set of 101 languages
desired_languages_with_codes = [
    ('haw', 'Latn', 'Hawaiian'),
    ('cos', 'Latn', 'Corsican'),
    ('hmn', 'Latn', 'Hmong'),
    ('fry', 'Latn', 'Western Frisian'),
    ('fil', 'Latn', 'Filipino'),
]

# rewrite the above languages with codes as a dictionary with name and code keys
data_to_insert = []
for code, character_code, name in desired_languages_with_codes:
    data_to_insert.append({
        'name': name, 
        'code': code, 
        'character_code': character_code,
    })

def upgrade() -> None:
    # get metadata from current connection
    meta = sa.MetaData(bind=op.get_bind())

    # pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(only=('language_code',))

    # define table representation
    language_code_tbl = sa.Table('language_code', meta)

    # insert each 3 letter code and language to the db
    op.bulk_insert(language_code_tbl, data_to_insert)


def downgrade() -> None:
    op.execute("DELETE FROM language_code WHERE code IN ('haw', 'cos', 'hmn', 'fry', 'fil')")
