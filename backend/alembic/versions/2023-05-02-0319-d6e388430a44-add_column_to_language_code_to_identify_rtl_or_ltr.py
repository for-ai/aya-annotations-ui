"""Add column to language_code to identify rtl or ltr

Revision ID: d6e388430a44
Revises: c3c4e62fadcf
Create Date: 2023-05-02 03:19:03.458931+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6e388430a44'
down_revision = 'c3c4e62fadcf'
branch_labels = None
depends_on = None

# list of 3-letter language codes that are rtl
# https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code
RTL_LANGUAGES = [
    'acm', # Mesopotamian Arabic
    'acq', # Ta'izzi-Adeni Arabic
    'ajp', # South Levantine Arabic
    'apc', # North Levantine Arabic
    'arb', # Standard Arabic
    'arz', # Egyptian Arabic
    'kmr', # Northern Kurdish
    'hau', # Hausa
    'heb', # Hebrew
    'kas', # Kashmiri
    'snd', # Sindhi
    'urd', # Urdu
    'ydd', # Eastern Yiddish
]

def upgrade() -> None:
    # create the enum type if it doesn't already exist
    op.execute(
        "CREATE TYPE direction AS ENUM ('ltr', 'rtl')"
    )

    # add a column to the language_code table to identify rtl or ltr
    op.add_column(
        "language_code",
        sa.Column(
            "direction",
            sa.Enum("ltr", "rtl", name="direction"),
            nullable=True,
        ),
    )

    # set the following languages to rtl
    op.execute(
        "UPDATE language_code SET direction = 'rtl' WHERE code IN ('{}')".format(
            "', '".join(RTL_LANGUAGES)
        )
    )

    # set the remaining languages to ltr
    op.execute(
        "UPDATE language_code SET direction = 'ltr' WHERE direction IS NULL"
    )


def downgrade() -> None:
    # drop the column from the language_code table
    op.drop_column("language_code", "direction")

    # drop the enum type
    op.execute(
        "DROP TYPE direction"
    )
