"""add_task_views

Revision ID: 8aff6eda53a6
Revises: b9fb1a5e91f4
Create Date: 2023-08-17 05:58:36.643735+00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '8aff6eda53a6'
down_revision = 'b9fb1a5e91f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        """
        CREATE OR REPLACE VIEW public.task_1_submission AS
        SELECT
            id,
            submitted_by,
            submitted_prompt,
            submitted_completion,
            prompt_edited,
            completion_edited,
            prompt_rating,
            completion_rating,
            created_at,
            edit_distance
        FROM
            public.task_audit
        UNION ALL
        SELECT
            id,
            submitted_by,
            submitted_prompt,
            submitted_completion,
            prompt_edited,
            completion_edited,
            prompt_rating,
            completion_rating,
            created_at,
            edit_distance
        FROM
            public.task_contribution_audit;
        """
    )

    connection.execute(
        """
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
        """
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        """
        DROP VIEW public.task_1_submission;
        """
    )

    connection.execute(
        """
        DROP VIEW public.task_3_submission;
        """
    )
