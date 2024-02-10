"""rename_task_submission

Revision ID: b85910c50121
Revises: 2bb74cbd6ca3
Create Date: 2023-05-06 18:14:25.826112+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b85910c50121'
down_revision = '2bb74cbd6ca3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # rename the task submission table to task audit
    op.rename_table("task_submission", "task_audit")

    # rename the index on the task submission table to task audit
    op.execute("ALTER INDEX task_submission_pkey RENAME TO task_audit_pkey")

    # rename the foreign key on the task submission table to task audit
    op.execute("ALTER TABLE task_audit RENAME CONSTRAINT task_submission_submitted_by_fkey TO task_audit_submitted_by_fkey")


def downgrade() -> None:
    # rename the task audit table to task submission
    op.rename_table("task_audit", "task_submission")

    # rename the index on the task audit table to task submission
    op.execute("ALTER INDEX task_audit_pkey RENAME TO task_submission_pkey")

    # rename the foreign key on the task audit table to task submission
    op.execute("ALTER TABLE task_submission RENAME CONSTRAINT task_audit_submitted_by_fkey TO task_submission_submitted_by_fkey")
