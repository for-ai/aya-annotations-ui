"""add_more_missing_lang_codes

Revision ID: c3c4e62fadcf
Revises: 5536f1b704eb
Create Date: 2023-04-30 21:52:14.611385+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3c4e62fadcf'
down_revision = '5536f1b704eb'
branch_labels = None
depends_on = None

desired_languages_with_codes = [
    ('sun', 'Arab', 'Sundanese'),
    ('taq', 'Latn', 'Tamasheq'),
    ('als', 'Latn', 'Tosk Albanian'),
    ('min', 'Latn', 'Minangkabau'),
    ('mni', 'Beng', 'Manipuri'),
    ('nno', 'Latn', 'Norwegian Nynorsk'),
    ('plt', 'Latn', 'Plateau Malagasy'),
    ('sin', 'Sinh', 'Sinhala'),
    ('slv', 'Latn', 'Slovenian'),
    ('smo', 'Latn', 'Samoan'),
    ('sot', 'Latn', 'Southern Sotho'),
    ('ydd', 'Hebr', 'Eastern Yiddish'),
    ('yue', 'Hant', 'Cantonese'),
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
    op.execute("DELETE FROM language_code WHERE code IN ('sun', 'taq', 'als', 'min', 'mni', 'nno', 'plt', 'sin', 'slv', 'smo', 'sot', 'ydd', 'yue')")


