"""populate_country_codes

Revision ID: eb13778e0573
Revises: 1276d056240a
Create Date: 2023-04-17 01:57:05.638839+00:00

"""
from alembic import op
import sqlalchemy as sa

import pycountry

# revision identifiers, used by Alembic.
revision = "eb13778e0573"
down_revision = "1276d056240a"
branch_labels = None
depends_on = None

data = [(c.alpha_2, c.name) for c in pycountry.countries]
data_to_insert = [
    {
        "code": code,
        "name": name,
    }
    for code, name in data
]


def upgrade() -> None:
    # get metadata from current connection
    meta = sa.MetaData(bind=op.get_bind())

    # pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(only=("country_code",))

    # define table representation
    country_code_tbl = sa.Table("country_code", meta)

    op.bulk_insert(country_code_tbl, data_to_insert)


def downgrade() -> None:
    op.execute("DELETE FROM country_code")
