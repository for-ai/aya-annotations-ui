"""add_task_num_and_language_id_column_for_task

Revision ID: b5eb22ad2a73
Revises: 5cbe4ab55392
Create Date: 2023-04-07 05:26:13.664241+00:00

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'b5eb22ad2a73'
down_revision = '5cbe4ab55392'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add a language_id column to the task table
    # this column is used to keep track of the language
    # of the task and is a foreign key to the language_code table
    op.add_column('task', sa.Column('language_id', UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('fk_task_language_id', 'task', 'language_code', ['language_id'], ['id'])
    
    # a new column is added to the task table
    # with the name task_num and of the type identity.
    # this column is used to keep track of the number of tasks
    # and so we can use it to select random tasks from the database
    # without having to use the random() function.
    op.execute("ALTER TABLE task ADD COLUMN task_num INT GENERATED ALWAYS AS IDENTITY")

    # create an index on the task_num column for faster lookups
    op.execute("CREATE INDEX IF NOT EXISTS task_num_index ON task (task_num, language_id)")


def downgrade() -> None:
    op.execute("ALTER TABLE task DROP COLUMN task_num")
    op.execute("DROP INDEX IF EXISTS task_num_language_index")
    op.drop_column('task', 'language_id')
