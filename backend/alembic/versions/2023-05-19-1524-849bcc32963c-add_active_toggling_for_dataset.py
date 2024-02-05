"""add_active_toggling_for_dataset

Revision ID: 849bcc32963c
Revises: f233a368f1c4
Create Date: 2023-05-19 15:24:01.728156+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '849bcc32963c'
down_revision = 'f233a368f1c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # add an is_active column to the dataset table
    # that defaults to true
    op.add_column(
        'dataset',
        sa.Column(
            'active',
            sa.Boolean,
            nullable=False,
            server_default=sa.true(),
        ),
    )

    # set any of the datasets using `facebook-nllb-200-3.3B` to inactive,
    # but make sure we're not deactivating `sentencesplit_facebook-nllb-200-3.3B`
    op.execute(
        """
        UPDATE dataset
        SET active = false
        WHERE name LIKE '%facebook-nllb-200-3.3B%'
        AND name NOT LIKE '%sentencesplit_facebook-nllb-200-3.3B%'
        """
    )


def downgrade() -> None:
    # remove the active column from the dataset table
    op.drop_column('dataset', 'active')

