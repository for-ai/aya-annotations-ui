"""drop_audit_review_limit

Revision ID: ba32cbdb7ef4
Revises: e7409f573d47
Create Date: 2023-08-27 22:40:11.836705+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba32cbdb7ef4'
down_revision = 'e7409f573d47'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # drop the audit_review_limit table
    op.drop_table('audit_review_limit')


def downgrade() -> None:
    # no need to downgrade. this is a one-way migration.
    pass
