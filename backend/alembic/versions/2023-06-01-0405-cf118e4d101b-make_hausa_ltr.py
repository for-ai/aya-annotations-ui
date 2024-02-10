"""make_hausa_ltr

Revision ID: cf118e4d101b
Revises: 785f6b48ad7a
Create Date: 2023-06-01 04:05:49.718957+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf118e4d101b'
down_revision = '785f6b48ad7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # make Hausa (hau) ltr direction in the language_code table
    op.execute("UPDATE language_code SET direction = 'ltr' WHERE code = 'hau'")
    

def downgrade() -> None:
    # make Hausa (hau) rtl direction in the language_code table
    op.execute("UPDATE language_code SET direction = 'rtl' WHERE code = 'hau'")
