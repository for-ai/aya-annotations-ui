"""identify_primary_101_langs

Revision ID: 672360a33e72
Revises: b389845cf201
Create Date: 2023-11-18 04:20:21.574869+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '672360a33e72'
down_revision = 'b389845cf201'
branch_labels = None
depends_on = None


primary_langs = [
	'Afrikaans',
	'Albanian',
	'Amharic',
	'Standard Arabic',
	'Mesopotamian Arabic',
	'Moroccan Arabic',
	'Najdi Arabic',
	'North Levantine Arabic',
	'South Levantine Arabic',
	"Ta''izzi Arabic",
	'Tunisian Arabic',
	'Armenian',
	'North Azerbaijani',
	'South Azerbaijani',
	'Basque',
	'Belarusian',
	'Bengali',
	'Bulgarian',
	'Burmese',
	'Catalan',
	'Cebuano',
	'Nyanja',
	'Simplified Chinese',
	'Traditional Chinese',
	'Corsican',
	'Czech',
	'Danish',
	'Dutch',
	'English',
	'Esperanto',
	'Estonian',
	'Filipino',
	'Finnish',
	'French',
	'Galician',
	'Georgian',
	'German',
	'Modern Greek (1453-)',
	'Gujarati',
	'Haitian Creole', 
	'Hausa',
	'Hawaiian',
	'Hebrew',
	'Hindi',
	'Hmong',
	'Hungarian',
	'Icelandic',
	'Igbo',
	'Indonesian',
	'Irish',
	'Italian',
	'Japanese',
	'Javanese',
	'Kannada',
	'Kazakh',
	'Central Khmer',
	'Korean',
	'Kurdish',
	'Kyrgyz',
	'Lao',
	'Latin',
	'Standard Latvian',
	'Lithuanian',
	'Luxembourgish',
	'Macedonian',
	'Plateau Malagasy',
	'Malay',
	'Malayalam',
	'Maltese',
	'Maori',
	'Marathi',
	'Mongolian',
	'Nepali',
	'Norwegian',
	'Pashto',
	'Iranian Persian',
	'Polish',
	'Portuguese',
	'Panjabi',
	'Romanian',
	'Russian',
	'Samoan',
	'Scottish Gaelic', 
	'Serbian',
	'Shona',
	'Sindhi',
	'Sinhala',
	'Slovak',
	'Slovenian',
	'Somali',
	'Sotho',
	'Spanish',
	'Sundanese',
	'Swahili',
	'Swedish',
	'Tajik',
	'Tamil',
	'Telugu',
	'Thai',
	'Turkish',
	'Ukrainian',
	'Urdu',
	'Northern Uzbek',
	'Vietnamese',
	'Welsh',
	'Western Frisian', 
	'Xhosa',
	'Eastern Yiddish',
	'Yoruba',
	'Zulu',
]

def upgrade() -> None:
    # add a boolean column to the language_code table to identify
    # which languages are part of our original 101 languages
    op.add_column('language_code', sa.Column('is_primary_101', sa.Boolean(), nullable=True))

    # set the boolean column to true for all primary languages
    op.execute(
        "UPDATE language_code SET is_primary_101 = TRUE WHERE name IN ('{}')".format("', '".join(primary_langs))
    )

    # set the boolean column to false for all non-primary languages
    op.execute(
        "UPDATE language_code SET is_primary_101 = FALSE WHERE is_primary_101 IS NULL"
    )



def downgrade() -> None:
    op.drop_column('language_code', 'is_primary_101')
