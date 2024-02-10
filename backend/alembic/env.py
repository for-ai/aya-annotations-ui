import os

from pathlib import Path
from logging.config import fileConfig

import sqlalchemy as sa

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

ENVIRONMENT = os.environ.get("ENVIRONMENT")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

if config.attributes.get('configure_logger', True):
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

valid_environments = [
    "test",
    "local",
    "staging",
    "production",
]
if not any([ENVIRONMENT == env for env in valid_environments]):
    raise ValueError(
        f"Invalid environment set: {ENVIRONMENT}. "
        f"Valid environments are: {', '.join(valid_environments)}"
    )

dotenv_filepath = Path(__file__).parent.parent / f".env.{ENVIRONMENT}"
load_dotenv(dotenv_filepath)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    environment = os.environ["ENVIRONMENT"]

    if environment == "production":
        print("Running migrations in PRODUCTION mode. Ensure this operation is correct.")
    elif environment == "staging":
        print("Running migrations in staging mode. Ensure this operation is correct.")
    elif environment == "local":
        print("Running migrations in local mode.")

    db_uri = os.environ["INSTRUCT_MULTILINGUAL_APP_DB_URI"]

    context.configure(
        url=db_uri,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    if ENVIRONMENT == "production":
        print("Running migrations in PRODUCTION mode. Ensure this operation is correct.")
    elif ENVIRONMENT == "local":
        print("Running migrations in local mode.")
    elif ENVIRONMENT == "test":
        print("Running migrations in test mode.")

    db_uri = os.environ["INSTRUCT_MULTILINGUAL_APP_DB_URI"]

    if db_uri is None:
        raise ValueError(
            "No database URI set. Check your .env.local or .env.prod file."
        )

    connectable = sa.create_engine(
        db_uri,
        client_encoding="utf8",
        pool_size=1,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
