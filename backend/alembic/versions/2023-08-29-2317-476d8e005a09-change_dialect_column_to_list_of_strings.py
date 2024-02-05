"""Change dialect column to list of strings

Revision ID: 476d8e005a09
Revises: e7409f573d47
Create Date: 2023-08-29 23:17:33.706542+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '476d8e005a09'
down_revision = 'ba32cbdb7ef4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the old dialect column from the users table
    op.drop_column('user', 'dialect')
    
    # Add the new dialects array column to the users table
    op.add_column(
        'user', 
        sa.Column('dialects', sa.ARRAY(sa.String(50)))
    )


def downgrade() -> None:
    # Drop the dialects array column from the users table
    op.drop_column('user', 'dialects')
    
    # Add back the old dialect column to the users table
    op.add_column(
        'user', 
        sa.Column('dialect', sa.String(length=256))
    )

