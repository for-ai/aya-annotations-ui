"""add_contrib_details_to_task_3

Revision ID: b5cbc7a4fb61
Revises: 8aff6eda53a6
Create Date: 2023-08-23 09:58:06.051864+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b5cbc7a4fb61'
down_revision = '8aff6eda53a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the existing view
    op.execute("DROP VIEW IF EXISTS public.task_3_submission;")

    # Create the updated view
    op.execute("""
    CREATE OR REPLACE VIEW public.task_3_submission AS
        SELECT
            tar.id,
            tar.edited_prompt_rating,
            tar.edited_completion_rating,
            tar.improved_prompt,
            tar.improved_completion,
            tar.improvement_feedback,
            tar.submitted_by,
            tar.created_at,
            ta.submitted_prompt AS edited_prompt,
            ta.submitted_completion AS edited_completion,
            t.prompt AS original_prompt,
            t.completion AS original_completion
        FROM
            public.task_audit_review tar
        INNER JOIN
            public.task_audit ta ON tar.task_audit_id = ta.id
        INNER JOIN
            public.task t ON ta.task_id = t.id

        UNION ALL

        SELECT
            tcar.id,
            tcar.edited_prompt_rating,
            tcar.edited_completion_rating,
            tcar.improved_prompt,
            tcar.improved_completion,
            tcar.improvement_feedback,
            tcar.submitted_by,
            tcar.created_at,
            tca.submitted_prompt AS edited_prompt,
            tca.submitted_completion AS edited_completion,
            tc.submitted_prompt AS original_prompt,
            tc.submitted_completion AS original_completion
        FROM
            public.task_contribution_audit_review tcar
        INNER JOIN
            public.task_contribution_audit tca ON tcar.task_contribution_audit_id = tca.id
        INNER JOIN
            public.task_contribution tc ON tca.task_contribution_id = tc.id;
    """)


def downgrade() -> None:
    # Drop the updated view
    op.execute("DROP VIEW public.task_3_submission;")

    # Create the original view
    op.execute("""
    CREATE OR REPLACE VIEW public.task_3_submission AS
        SELECT
            id,
            edited_prompt_rating,
            edited_completion_rating,
            improved_prompt,
            improved_completion,
            improvement_feedback,
            submitted_by,
            created_at
        FROM
            public.task_audit_review
        UNION ALL
        SELECT
            id,
            edited_prompt_rating,
            edited_completion_rating,
            improved_prompt,
            improved_completion,
            improvement_feedback,
            submitted_by,
            created_at
        FROM
            public.task_contribution_audit_review;
    """)
