"""store_discord_email_and_id

Revision ID: 68daab0b8ccb
Revises: 38bb36535ede
Create Date: 2023-06-16 13:58:18.633420+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68daab0b8ccb'
down_revision = '38bb36535ede'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('email', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('discord_id', sa.String(), nullable=True))

    # drop the unique constraint on the username column
    op.drop_constraint('user_username_key', 'user')

    # ensure that the discord_id column is unique
    op.create_unique_constraint('uq_user_discord_id', 'user', ['discord_id'])


def downgrade() -> None:
    op.drop_column('user', 'email')
    op.drop_column('user', 'discord_id')

    # drop the unique constraint
    op.drop_constraint('uq_user_discord_id', 'user')

    # ensure that the username column is unique
    op.create_unique_constraint('user_username_key', 'user', ['username'])
