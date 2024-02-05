"""add created_at for audit_review_limit

Revision ID: 5c6ab0fe5920
Revises: c2583aaea36f
Create Date: 2023-07-06 13:27:56.193812+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c6ab0fe5920'
down_revision = 'c2583aaea36f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add created_at for audit_review_limit
    op.execute("""
    ALTER TABLE audit_review_limit
    ADD COLUMN created_at TIMESTAMP WITHOUT TIME ZONE;
    """)

    # assign a default value to backfill the created_at column
    op.execute("""
    UPDATE audit_review_limit
    SET created_at = '2023-07-06 06:24:27.895848'
    """)

    # add a constraint to the created_at column
    op.execute("""
    ALTER TABLE audit_review_limit
    ALTER COLUMN created_at SET NOT NULL;
    """)


def downgrade() -> None:
    # remove the created_at column
    op.drop_column('audit_review_limit', 'created_at')
