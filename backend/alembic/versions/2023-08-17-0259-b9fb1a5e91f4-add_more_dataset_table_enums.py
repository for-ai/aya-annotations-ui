"""add_more_dataset_table_enums

Revision ID: b9fb1a5e91f4
Revises: 4c8caa38e453
Create Date: 2023-08-17 02:59:20.054811+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9fb1a5e91f4'
down_revision = '4c8caa38e453'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add an additional enum value to the task_type enum
    # in the task table
    op.execute("ALTER TYPE task_type ADD VALUE 'audit_crowdsourced_data';")


def downgrade() -> None:
    # remove the additional enum value from the task_type enum
    # in the task table
    op.execute("ALTER TYPE task_type DROP VALUE 'audit_crowdsourced_data';")
