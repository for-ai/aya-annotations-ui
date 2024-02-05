"""recreate_prompt_completion_index

Revision ID: 2bb74cbd6ca3
Revises: d6e388430a44
Create Date: 2023-05-05 04:07:56.496927+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '2bb74cbd6ca3'
down_revision = 'd6e388430a44'
branch_labels = None
depends_on = None


def upgrade():
    # create the key_hash column
    op.add_column('task', sa.Column('key_hash', sa.String(length=64), nullable=True))

    # set the key_hash column to the first 16 characters of the sha256 hash of the prompt and completion
    op.execute('UPDATE task SET key_hash = SUBSTRING(encode(digest(CONCAT(prompt, completion, dataset_id, language_id), \'sha256\'), \'hex\'), 1, 16)')

    # ensure that the key_hash column is not nullable
    op.alter_column('task', 'key_hash', nullable=False)

    # ensure that the key_hash column is unique
    op.create_index('uq_task_prompt_completion_key_hash', 'task', ['key_hash'], unique=True)

    # ensure that the prompt and completion unique constraint and index is dropped
    op.drop_constraint('uq_task_prompt_completion_key', 'task', type_='unique')

    # Define a SQL function to calculate the SHA256 hash of the `prompt` and `completion` columns
    sql = text("""
        CREATE OR REPLACE FUNCTION calculate_hash_key() RETURNS TRIGGER AS $$
        BEGIN
            NEW.key_hash :=
                SUBSTRING(
                    encode(
                        digest(CONCAT(NEW.prompt, NEW.completion), 'sha256'),
                        'hex'
                    ),
                    1,
                    16
                );
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Execute the SQL function
    conn = op.get_bind()
    conn.execute(sql)

    # Create a database trigger that calls the `calculate_hash_key` function on every insert or update operation
    op.execute("""
        CREATE TRIGGER task_hash_key_trigger
        BEFORE INSERT OR UPDATE ON task
        FOR EACH ROW
        EXECUTE FUNCTION calculate_hash_key();
    """)

def downgrade():    
    # add the unique constraint on the prompt and completion columns, which is what we had before
    # and automatically creates an index on those columns
    op.create_unique_constraint('uq_task_prompt_completion_key', 'task', ['prompt', 'completion'])

    # drop the unique constraint on the key_hash column
    op.drop_index('uq_task_prompt_completion_key_hash', table_name='task')

    # Drop the database trigger that calls the `calculate_hash_key` function
    op.execute('DROP TRIGGER task_hash_key_trigger ON task')

    # Drop the `calculate_hash_key` function
    op.execute("DROP FUNCTION calculate_hash_key()")

    # drop the key_hash column
    op.drop_column('task', 'key_hash')