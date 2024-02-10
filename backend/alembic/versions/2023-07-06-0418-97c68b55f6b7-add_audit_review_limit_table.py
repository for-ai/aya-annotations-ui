"""add_audit_review_limit_table

Revision ID: 97c68b55f6b7
Revises: 1dd7526c13d5
Create Date: 2023-07-06 04:18:01.361815+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97c68b55f6b7'
down_revision = '1dd7526c13d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add a table called `audit_review_limit` with the following columns:
    # - id: uuid
    # - user_id: uuid (fk to public.user)
    # - remaining_annotation_validations: integer
    # - last_updated_at: timestamp without time zone
    #
    # This will allows us to keep track of how many audit reviews a user has left to receive,
    # summed up across all languages (which they contributed to).
    # We'll use this to see how many more ratings we need to get a sense of their quality as an auditor.
    op.execute("""
        CREATE TABLE audit_review_limit (
            id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id uuid REFERENCES "user" (id),
            remaining_audit_reviews integer NOT NULL,
            last_updated_at timestamp without time zone NOT NULL DEFAULT now()
        );
    """)

    # load the table with an initial value for each user
    # that is the number of audit reviews they have left to receive
    # for the generated or contributed tasks they audited
    op.execute("""
        INSERT INTO audit_review_limit (user_id, remaining_audit_reviews)
        SELECT
            user_id,
            count(*) AS remaining_audit_reviews
        FROM (
            SELECT
                u.id as user_id,
                ROW_NUMBER() OVER (
                PARTITION BY ta.submitted_by
                ORDER BY ta.created_at DESC
                ) AS row_num,
                COUNT(*) OVER (PARTITION BY ta.submitted_by) AS audit_count
            FROM task_audit ta
            JOIN task t ON ta.task_id = t.id
            JOIN public.user u ON ta.submitted_by = u.id
            LEFT JOIN task_audit_review tar ON ta.id = tar.task_audit_id
            WHERE tar.task_audit_id IS NULL

            UNION

            SELECT
                u.id as user_id,
                ROW_NUMBER() OVER (
                PARTITION BY tac.submitted_by
                ORDER BY tac.created_at DESC
                ) AS row_num,
                COUNT(*) OVER (PARTITION BY tac.submitted_by) AS audit_count
            FROM task_contribution_audit tac
            JOIN task_contribution tc ON tac.task_contribution_id = tc.id
            JOIN public.user u ON tac.submitted_by = u.id
            LEFT JOIN task_contribution_audit_review tcar ON tac.id = tcar.task_contribution_audit_id
            WHERE tcar.task_contribution_audit_id IS NULL
        ) AS subquery
        WHERE row_num <= FLOOR(10 * LOG(10, audit_count) + 1)
        GROUP BY user_id
        ORDER BY remaining_audit_reviews DESC;
    """)

def downgrade() -> None:
    # remove the `audit_review_limit` table
    op.execute("DROP TABLE audit_review_limit;")
