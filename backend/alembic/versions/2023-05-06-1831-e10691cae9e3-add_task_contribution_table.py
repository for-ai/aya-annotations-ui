"""add_task_contribution_table

Revision ID: e10691cae9e3
Revises: b85910c50121
Create Date: 2023-05-06 18:31:42.210642+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'e10691cae9e3'
down_revision = 'b85910c50121'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # create the task contribution table
    op.create_table(
        "task_contribution",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("submitted_by", UUID(as_uuid=True), sa.ForeignKey("user.id"), nullable=False),
        sa.Column("submitted_prompt", sa.Text, nullable=False),
        sa.Column("submitted_completion", sa.Text, nullable=False),
        sa.Column("language_id", UUID(as_uuid=True), sa.ForeignKey("language_code.id"), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    # drop the task contribution table
    op.drop_table("task_contribution")
