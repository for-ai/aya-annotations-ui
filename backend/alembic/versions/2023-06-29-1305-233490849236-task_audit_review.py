"""task_audit_review

Revision ID: 233490849236
Revises: 0bf3df1a1e43
Create Date: 2023-06-29 13:05:36.361283+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '233490849236'
down_revision = '3380a3512991'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'task_audit_review',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('task_audit_id', UUID(as_uuid=True), sa.ForeignKey('task_audit.id'), nullable=False),
        sa.Column('edited_prompt_rating', sa.Integer, nullable=False),
        sa.Column('edited_completion_rating', sa.Integer, nullable=False),
        # these should only end up with null values if the ratings are < 5
        sa.Column('improved_prompt', sa.Text, nullable=True),
        sa.Column('improved_completion', sa.Text, nullable=True),
        sa.Column('improvement_feedback', sa.Text, nullable=False),
        sa.Column('submitted_by', UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'task_contribution_audit_review',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('task_contribution_audit_id', UUID(as_uuid=True), sa.ForeignKey('task_contribution_audit.id'), nullable=False),
        sa.Column('edited_prompt_rating', sa.Integer, nullable=False),
        sa.Column('edited_completion_rating', sa.Integer, nullable=False),
        # these should only end up with null values if the ratings are < 5
        sa.Column('improved_prompt', sa.Text, nullable=True),
        sa.Column('improved_completion', sa.Text, nullable=True),
        sa.Column('improvement_feedback', sa.Text, nullable=False),
        sa.Column('submitted_by', UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('task_audit_review')
    op.drop_table('task_contribution_audit_review')