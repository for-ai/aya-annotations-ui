"""add_more_user_survey_questions

Revision ID: 785f6b48ad7a
Revises: 08d92ecbd824
Create Date: 2023-05-30 03:40:39.025935+00:00

"""
from alembic import op
import sqlalchemy as sa

import sqlalchemy.dialects.postgresql as sa_psql


# revision identifiers, used by Alembic.
revision = '785f6b48ad7a'
down_revision = '08d92ecbd824'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add age_range column to user table
    op.add_column(
        'user',
        sa.Column(
            'age_range',
            sa_psql.INT4RANGE,
            nullable=True,
        ),
    )

    # add the gender column to user table
    op.add_column(
        'user',
        sa.Column(
            'gender',
            sa_psql.VARCHAR(64),
            nullable=True,
        ),
    )


def downgrade() -> None:
    # drop the age_range column from user table
    op.drop_column(
        'user',
        'age_range',
    )

    # drop the gender column from user table
    op.drop_column(
        'user',
        'gender',
    )