import asyncio

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import Session, create_engine

from instruct_multilingual.config import get_settings

test_settings = get_settings()

if test_settings.config.environment != "test":
    raise ValueError(f"ENVIRONMENT must be 'test' to run tests. Got {test_settings.config.environment}")


@pytest.fixture(scope="session")
def engine():
    postgres_url = test_settings.instruct_multilingual_app_db_uri
    engine = create_engine(
        postgres_url,
        client_encoding="utf8",
        pool_pre_ping=True,
        isolation_level="REPEATABLE READ",
    )

    if not database_exists(engine.url):
        print("creating test database")
        create_database(engine.url, template="template0")
        print("test database created")

    yield engine


@pytest.fixture(scope="session")
def db(engine):
    connection = engine.connect()
    session = Session(bind=connection)

    session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    session.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    session.commit()

    yield session

    session.close()

    if database_exists(engine.url):
        print("dropping test database")
        drop_database(engine.url)
        print("test database dropped")

    connection.close()


@pytest.fixture(scope="session")
def test_client(db):
    from main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    """
    Override the default event loop with a new one.

    See: https://github.com/tortoise/tortoise-orm/issues/638
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_test_client(db):
    from main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client