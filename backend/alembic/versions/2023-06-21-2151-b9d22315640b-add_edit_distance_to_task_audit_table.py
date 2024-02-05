"""add_edit_distance_to_task_audit_table

Revision ID: b9d22315640b
Revises: 53f48b99dd8c
Create Date: 2023-06-21 21:51:51.195493+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9d22315640b'
down_revision = '53f48b99dd8c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add edit_distance as a decimal column to the task_audit table
    op.add_column(
        'task_audit',
        sa.Column('edit_distance', sa.DECIMAL, nullable=True)
    )


def downgrade() -> None:
    # drop edit_distance column from the task_audit table
    op.drop_column('task_audit', 'edit_distance')
