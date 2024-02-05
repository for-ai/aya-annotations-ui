"""separate_chinese_hans_hant

Revision ID: 90905dca267b
Revises: 849bcc32963c
Create Date: 2023-05-22 02:35:39.625536+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90905dca267b'
down_revision = '849bcc32963c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # set the current "Chinese" language to "Chinese (Traditional)" in the language_code table
    # since it uses the Hant character code
    op.execute(
        """
        UPDATE language_code
        SET name = 'Chinese (Traditional)'
        WHERE name = 'Chinese'
        """
    )

    # add a new language to the language_code table for "Chinese (Simplified)"
    op.execute(
        """
        INSERT INTO language_code (code, name, character_code, direction)
        VALUES ('zho', 'Chinese (Simplified)', 'Hans', 'ltr')
        """
    )

    # update the dataset table to use the new language_code ids
    op.execute(
        """
        UPDATE dataset
        SET language_id = (
            SELECT id
            FROM language_code
            WHERE name = 'Chinese (Traditional)'
        )
        WHERE name like '%zho_Hant%'
        """
    )

    op.execute(
        """
        UPDATE dataset
        SET language_id = (
            SELECT id
            FROM language_code
            WHERE name = 'Chinese (Simplified)'
        )
        WHERE name like '%zho_Hans%'
        """
    )

    # update the task table to use the new language_code ids
    # Hant tasks will already be using the correct language_code id
    # so we only need to update the Hans tasks.
    # use the dataset's language_id since it will be the correct one
    op.execute(
        """
        UPDATE task
        SET language_id = dataset.language_id
        FROM dataset
        WHERE task.dataset_id = dataset.id
        AND dataset.active = TRUE
        AND dataset.name LIKE '%zho_Hans%';
        """
    )

def downgrade() -> None:
    # set the current "Chinese (Traditional)" language to "Chinese" in the language_code table
    op.execute(
        """
        UPDATE language_code
        SET name = 'Chinese'
        WHERE name = 'Chinese (Traditional)'
        """
    )

    # update the dataset table to use the new language_code ids
    op.execute(
        """
        UPDATE dataset
        SET language_id = (
            SELECT id
            FROM language_code
            WHERE name = 'Chinese'
        )
        WHERE name like '%zho_Hant%'
        """
    )

    op.execute(
        """
        UPDATE dataset
        SET language_id = (
            SELECT id
            FROM language_code
            WHERE name = 'Chinese'
        )
        WHERE name like '%zho_Hans%'
        """
    )

    # update the task table to just use the Chinese language_code id
    op.execute(
        """
        UPDATE task
        SET language_id = dataset.language_id
        FROM dataset
        WHERE task.dataset_id = dataset.id
        AND dataset.active = TRUE
        AND dataset.name LIKE '%zho_Hans%'
        """
    )

    # delete the "Chinese (Traditional)" language from the language_code table
    op.execute(
        """
        DELETE FROM language_code
        WHERE name = 'Chinese (Simplified)'
        """
    )
