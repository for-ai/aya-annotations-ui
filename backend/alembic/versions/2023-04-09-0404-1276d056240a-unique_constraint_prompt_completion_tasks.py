"""unique_constraint_prompt_completion_tasks

Revision ID: 1276d056240a
Revises: b5eb22ad2a73
Create Date: 2023-04-09 04:04:16.921687+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1276d056240a'
down_revision = 'b5eb22ad2a73'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # drop the old constraint for prompt and completion columns on the task table
    op.drop_constraint('task_prompt_key', 'task', type_='unique')
    op.drop_constraint('task_completion_key', 'task', type_='unique')

    # create a new constraint for prompt and completion columns on the task table
    op.create_unique_constraint('uq_task_prompt_completion_key', 'task', ['prompt', 'completion'])


def downgrade() -> None:
    # drop the new constraint for prompt and completion columns on the task table
    op.drop_constraint('uq_task_prompt_completion_key', 'task', type_='unique')

    # create a new constraint for prompt and completion columns on the task table
    op.create_unique_constraint('task_prompt_key', 'task', ['prompt'])
    op.create_unique_constraint('task_completion_key', 'task', ['completion'])
