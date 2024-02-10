"""deactivate_xp3_flores_data

Revision ID: 1dd7526c13d5
Revises: 9fdf109afc92
Create Date: 2023-07-06 03:55:24.257547+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dd7526c13d5'
down_revision = '9fdf109afc92'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # deactivate datasets that are from 'dataset/sample_100/xp3_facebook_flores'
    op.execute("UPDATE dataset SET active = false WHERE name LIKE '%%dataset/sample_100/xp3_facebook_flores%';")

def downgrade() -> None:
    # activate datasets that are from 'dataset/sample_100/xp3_facebook_flores'
    op.execute("UPDATE dataset SET active = true WHERE name LIKE '%%dataset/sample_100/xp3_facebook_flores%';")
