"""add_language_codes_bulk

Revision ID: 5cbe4ab55392
Revises: 48082df0bbba
Create Date: 2023-04-01 20:50:55.964835+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cbe4ab55392'
down_revision = '48082df0bbba'
branch_labels = None
depends_on = None

# initial set of 101 languages
desired_languages_with_codes = [
    ('ace', 'Arab', 'Achinese'),
    ('ace', 'Latn', 'Achinese'),
    ('acm', 'Arab', 'Mesopotamian Arabic'),
    ('acq', 'Arab', "Ta'izzi-Adeni Arabic"),
    ('aeb', 'Arab', 'Tunisian Arabic'),
    ('afr', 'Latn', 'Afrikaans'),
    ('ajp', 'Arab', 'South Levantine Arabic'),
    ('aka', 'Latn', 'Akan'),
    ('amh', 'Ethi', 'Amharic'),
    ('apc', 'Arab', 'North Levantine Arabic'),
    ('arb', 'Arab', 'Standard Arabic'),
    ('arb', 'Latn', 'Standard Arabic'),
    ('ars', 'Arab', 'Najdi Arabic'),
    ('ary', 'Arab', 'Moroccan Arabic'),
    ('arz', 'Arab', 'Egyptian Arabic'),
    ('asm', 'Beng', 'Assamese'),
    ('ast', 'Latn', 'Asturian'),
    ('awa', 'Deva', 'Awadhi'),
    ('ayr', 'Latn', 'Central Aymara'),
    ('azb', 'Arab', 'South Azerbaijani'),
    ('azj', 'Latn', 'North Azerbaijani'),
    ('bak', 'Cyrl', 'Bashkir'),
    ('bam', 'Latn', 'Bambara'),
    ('ban', 'Latn', 'Balinese'),
    ('bel', 'Cyrl', 'Belarusian'),
    ('bem', 'Latn', 'Bemba (Zambia)'),
    ('ben', 'Beng', 'Bengali'),
    ('bho', 'Deva', 'Bhojpuri'),
    ('bjn', 'Arab', 'Banjar'),
    ('bjn', 'Latn', 'Banjar'),
    ('bod', 'Tibt', 'Tibetan'),
    ('bos', 'Latn', 'Bosnian'),
    ('bug', 'Latn', 'Buginese'),
    ('bul', 'Cyrl', 'Bulgarian'),
    ('cat', 'Latn', 'Catalan'),
    ('ceb', 'Latn', 'Cebuano'),
    ('ces', 'Latn', 'Czech'),
    ('cjk', 'Latn', 'Chokwe'),
    ('ckb', 'Arab', 'Central Kurdish'),
    ('crh', 'Latn', 'Crimean Tatar'),
    ('cym', 'Latn', 'Welsh'),
    ('dan', 'Latn', 'Danish'),
    ('deu', 'Latn', 'German'),
    ('dik', 'Latn', 'Southwestern Dinka'),
    ('dyu', 'Latn', 'Dyula'),
    ('dzo', 'Tibt', 'Dzongkha'),
    ('ell', 'Grek', 'Modern Greek (1453-)'),
    ('eng', 'Latn', 'English'),
    ('epo', 'Latn', 'Esperanto'),
    ('est', 'Latn', 'Estonian'),
    ('eus', 'Latn', 'Basque'),
    ('ewe', 'Latn', 'Ewe'),
    ('fao', 'Latn', 'Faroese'),
    ('fij', 'Latn', 'Fijian'),
    ('fin', 'Latn', 'Finnish'),
    ('fon', 'Latn', 'Fon'),
    ('fra', 'Latn', 'French'),
    ('fur', 'Latn', 'Friulian'),
    ('fuv', 'Latn', 'Nigerian Fulfulde'),
    ('gaz', 'Latn', 'West Central Oromo'),
    ('gla', 'Latn', 'Scottish Gaelic'),
    ('gle', 'Latn', 'Irish'),
    ('glg', 'Latn', 'Galician'),
    ('grn', 'Latn', 'Guarani'),
    ('guj', 'Gujr', 'Gujarati'),
    ('hat', 'Latn', 'Haitian'),
    ('hau', 'Latn', 'Hausa'),
    ('heb', 'Hebr', 'Hebrew'),
    ('hin', 'Deva', 'Hindi'),
    ('hne', 'Deva', 'Chhattisgarhi'),
    ('hrv', 'Latn', 'Croatian'),
    ('hun', 'Latn', 'Hungarian'),
    ('hye', 'Armn', 'Armenian'),
    ('ibo', 'Latn', 'Igbo'),
    ('ilo', 'Latn', 'Iloko'),
    ('ind', 'Latn', 'Indonesian'),
    ('isl', 'Latn', 'Icelandic'),
    ('ita', 'Latn', 'Italian'),
    ('jav', 'Latn', 'Javanese'),
    ('jpn', 'Jpan', 'Japanese'),
    ('kab', 'Latn', 'Kabyle'),
    ('kac', 'Latn', 'Kachin'),
    ('kam', 'Latn', 'Kamba (Kenya)'),
    ('kan', 'Knda', 'Kannada'),
    ('kas', 'Arab', 'Kashmiri'),
    ('kas', 'Deva', 'Kashmiri'),
    ('kat', 'Geor', 'Georgian'),
    ('kaz', 'Cyrl', 'Kazakh'),
    ('kbp', 'Latn', 'Kabiyè'),
    ('kea', 'Latn', 'Kabuverdianu'),
    ('khk', 'Cyrl', 'Halh Mongolian'),
    ('khm', 'Khmr', 'Central Khmer'),
    ('kik', 'Latn', 'Kikuyu'),
    ('kin', 'Latn', 'Kinyarwanda'),
    ('kir', 'Cyrl', 'Kirghiz'),
    ('kmb', 'Latn', 'Kimbundu'),
    ('kmr', 'Latn', 'Northern Kurdish'),
    ('knc', 'Arab', 'Central Kanuri'),
    ('knc', 'Latn', 'Central Kanuri'),
    ('kon', 'Latn', 'Kongo'),
    ('kor', 'Hang', 'Korean'),
    ('lao', 'Laoo', 'Lao'),
    ('lij', 'Latn', 'Ligurian'),
    ('lim', 'Latn', 'Limburgan'),
    ('lin', 'Latn', 'Lingala'),
    ('lit', 'Latn', 'Lithuanian'),
    ('lmo', 'Latn', 'Lombard'),
    ('ltg', 'Latn', 'Latgalian'),
    ('ltz', 'Latn', 'Luxembourgish'),
    ('lua', 'Latn', 'Luba-Lulua'),
    ('lug', 'Latn', 'Ganda'),
    ('luo', 'Latn', 'Luo (Kenya and Tanzania)'),
    ('lus', 'Latn', 'Lushai'),
    ('lvs', 'Latn', 'Standard Latvian'),
    ('mag', 'Deva', 'Magahi'),
    ('mal', 'Mlym', 'Malayalam'),
    ('mar', 'Deva', 'Marathi'),
    ('mkd', 'Cyrl', 'Macedonian'),
    ('mlt', 'Latn', 'Maltese'),
    ('mri', 'Latn', 'Maori'),
    ('mya', 'Mymr', 'Burmese'),
    ('nld', 'Latn', 'Dutch'),
    ('nob', 'Latn', 'Norwegian Bokmål'),
    ('npi', 'Deva', 'Nepali (individual language)'),
    ('nso', 'Latn', 'Pedi'),
    ('nya', 'Latn', 'Nyanja'),
    ('oci', 'Latn', 'Occitan (post 1500)'),
    ('ory', 'Orya', 'Odia'),
    ('pan', 'Guru', 'Panjabi'),
    ('pbt', 'Arab', 'Southern Pashto'),
    ('pes', 'Arab', 'Iranian Persian'),
    ('pol', 'Latn', 'Polish'),
    ('por', 'Latn', 'Portuguese'),
    ('ron', 'Latn', 'Romanian'),
    ('rus', 'Cyrl', 'Russian'),
    ('slk', 'Latn', 'Slovak'),
    ('sna', 'Latn', 'Shona'),
    ('snd', 'Arab', 'Sindhi'),
    ('som', 'Latn', 'Somali'),
    ('spa', 'Latn', 'Spanish'),
    ('srp', 'Cyrl', 'Serbian'),
    ('swe', 'Latn', 'Swedish'),
    ('swh', 'Latn', 'Swahili (individual language)'),
    ('tam', 'Taml', 'Tamil'),
    ('tel', 'Telu', 'Telugu'),
    ('tgk', 'Cyrl', 'Tajik'),
    ('tgl', 'Latn', 'Tagalog'),
    ('tha', 'Thai', 'Thai'),
    ('tur', 'Latn', 'Turkish'),
    ('ukr', 'Cyrl', 'Ukrainian'),
    ('umb', 'Latn', 'Umbundu'),
    ('urd', 'Arab', 'Urdu'),
    ('uzn', 'Latn', 'Northern Uzbek'),
    ('vie', 'Latn', 'Vietnamese'),
    ('wol', 'Latn', 'Wolof'),
    ('xho', 'Latn', 'Xhosa'),
    ('yor', 'Latn', 'Yoruba'),
    ('zho', 'Hant', 'Chinese'),
    ('zsm', 'Latn', 'Standard Malay'),
    ('zul', 'Latn', 'Zulu'),
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
    op.execute('DELETE FROM language_code')
