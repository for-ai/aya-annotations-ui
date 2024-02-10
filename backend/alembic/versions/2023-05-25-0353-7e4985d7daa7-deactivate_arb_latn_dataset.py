"""deactivate_arb_Latn_dataset

Revision ID: 7e4985d7daa7
Revises: 90905dca267b
Create Date: 2023-05-25 03:53:16.227154+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e4985d7daa7'
down_revision = '90905dca267b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Deactivate arb_Latn dataset in the dataset table
    op.execute(
        """
        UPDATE dataset
        SET active = false
        WHERE name LIKE '%to_arb_Latn%';
        """
    )

    # Deactivate min_Arab dataset in the dataset table
    op.execute(
        """
        UPDATE dataset
        SET active = false
        WHERE name LIKE '%to_min_Arab%';
        """
    )


def downgrade() -> None:
    # Activate arb_Latn dataset in the dataset table
    op.execute(
        """
        UPDATE dataset
        SET active = true
        WHERE name LIKE '%to_arb_Latn%';
        """
    )

    # Activate min_Arab dataset in the dataset table
    op.execute(
        """
        UPDATE dataset
        SET active = true
        WHERE name LIKE '%to_min_Arab%';
        """
    )
