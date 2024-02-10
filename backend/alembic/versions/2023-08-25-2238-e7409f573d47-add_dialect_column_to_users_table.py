"""Add dialect column to users table

Revision ID: e7409f573d47
Revises: b5cbc7a4fb61
Create Date: 2023-08-25 22:38:57.293462+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7409f573d47'
down_revision = 'b5cbc7a4fb61'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the dialect column to the users table, limited to 256 characters
    op.add_column(
        'user', 
        sa.Column('dialect', sa.String(length=256))
    )


def downgrade() -> None:
    # Drop the dialect column from the users table
    op.drop_column('user', 'dialect')
