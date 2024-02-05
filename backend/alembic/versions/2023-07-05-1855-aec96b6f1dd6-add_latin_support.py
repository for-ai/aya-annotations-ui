"""add_latin_support

Revision ID: aec96b6f1dd6
Revises: 35875912fb74
Create Date: 2023-07-05 18:55:35.637514+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aec96b6f1dd6'
down_revision = '35875912fb74'
branch_labels = None
depends_on = None

#                                                    Table "public.language_code"
#      Column     |            Type             | Collation | Nullable |      Default       | Storage  | Stats target | Description 
# ----------------+-----------------------------+-----------+----------+--------------------+----------+--------------+-------------
#  id             | uuid                        |           | not null | uuid_generate_v4() | plain    |              | 
#  code           | character varying(3)        |           | not null |                    | extended |              | 
#  name           | text                        |           | not null |                    | extended |              | 
#  created_at     | timestamp without time zone |           | not null | now()              | plain    |              | 
#  character_code | character varying(5)        |           | not null |                    | extended |              | 
#  direction      | direction                   |           |          |                    | plain    |              | 
# Indexes:

def upgrade() -> None:
    # add Latin to the language_code table
    op.execute("INSERT INTO language_code (code, name, character_code, direction) VALUES ('lat', 'Latin', 'Latn', 'ltr');")


def downgrade() -> None:
    # remove Latin from the language_code table
    op.execute("DELETE FROM language_code WHERE code = 'lat';")
