import os

from sqlmodel import create_engine
from instruct_multilingual.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.instruct_multilingual_app_db_uri,
    client_encoding="utf8",
    pool_pre_ping=True,
    isolation_level="REPEATABLE READ",
)
