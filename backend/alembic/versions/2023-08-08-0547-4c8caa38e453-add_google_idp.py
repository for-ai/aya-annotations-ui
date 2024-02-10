"""add_google_idp

Revision ID: 4c8caa38e453
Revises: 8f4f6a9c6a31
Create Date: 2023-08-08 05:47:20.374334+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c8caa38e453'
down_revision = '8f4f6a9c6a31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('google_id', sa.String(), nullable=True))

    # ensure that the email column is unique
    op.create_unique_constraint('uq_user_email', 'user', ['email'])

    # ensure that the google_id column is unique
    op.create_unique_constraint('uq_user_google_id', 'user', ['google_id'])


def downgrade() -> None:
    op.drop_column('user', 'google_id')

    # Drop the unique constraint on email column
    op.drop_constraint('uq_user_email', 'user')

    # Drop the unique constraint on google_id column
    op.drop_constraint('uq_user_google_id', 'user')
