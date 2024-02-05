"""Add task_contribution_audit table

Revision ID: 3380a3512991
Revises: 0bf3df1a1e43
Create Date: 2023-06-26 14:23:27.107054+00:00

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '3380a3512991'
down_revision = '0bf3df1a1e43'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'task_contribution_audit',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('task_contribution_id', UUID(as_uuid=True), sa.ForeignKey('task_contribution.id'), nullable=False),
        sa.Column('submitted_by', UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('submitted_prompt', sa.Text, nullable=False),
        sa.Column('submitted_completion', sa.Text, nullable=False),
        sa.Column('prompt_edited', sa.Boolean, nullable=False),
        sa.Column('completion_edited', sa.Boolean, nullable=False),
        sa.Column('prompt_rating', sa.Integer, nullable=False),
        sa.Column('completion_rating', sa.Integer, nullable=False),
        sa.Column('edit_distance', sa.DECIMAL, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('task_contribution_audit')
