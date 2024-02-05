"""fix_primary_101_langs

Revision ID: 5b80958da127
Revises: 672360a33e72
Create Date: 2023-12-24 04:29:59.634296+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b80958da127'
down_revision = '672360a33e72'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # update the list of languages in the primary 101 that we missed due to
    # a bug in the identify_primary_101_langs migration. the naming of the languages
    # was not accurate so we missed some languages.
    op.execute(
        "UPDATE language_code SET is_primary_101 = TRUE WHERE name IN ('Haitian', 'Southern Sotho', 'Norwegian Bokmål', 'Nepali (individual language)', 'Swahili (individual language)', 'Tagalog', 'Northern Sotho', 'Egyptian Arabic', 'Standard Malay', 'Central Kurdish', 'Southern Pashto', 'Tosk Albanian', 'Ta''izzi-Adeni Arabic')"
    )


def downgrade() -> None:
    op.execute(
        "UPDATE language_code SET is_primary_101 = FALSE WHERE name IN ('Haitian', 'Southern Sotho', 'Norwegian Bokmål', 'Nepali (individual language)', 'Swahili (individual language)', 'Tagalog', 'Northern Sotho', 'Egyptian Arabic', 'Standard Malay', 'Central Kurdish', 'Southern Pashto', 'Tosk Albanian', 'Ta''izzi-Adeni Arabic')"
    )
