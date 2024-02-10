import os
from typing import Optional

from pydantic import BaseSettings

class Settings(BaseSettings):
    # must be set in .env.local, .env.staging, or .env.production
    # in order for the backend to work
    instruct_multilingual_app_db_uri: str

    jwt_secret: str
    jwt_algorithm: str
    jwt_expiration_time: int

    discord_api_base_url: str
    discord_client_id: str
    discord_client_secret: str
    discord_redirect_uri: str
    discord_webhook_url: Optional[str]

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    frontend_url: str
    # for_ai_url is the URL of the frontend under the for.ai
    # domain, vs. frontend_url which is the auto-generated
    # gcp cloud run URL
    for_ai_url: str

    app_name: str = "instruct-multilingual"
    run_migrations_on_startup: bool = True

    class Config:
        # https://fastapi.tiangolo.com/advanced/settings/
        # .env.local takes priority over .env.production
        environment: str = os.environ.get("ENVIRONMENT")

        if environment == "local":
            env_file = ".env.local"
        elif environment == "staging":
            env_file = ".env.staging"
        elif environment == "production":
            env_file = ".env.production"
        elif environment == "test":
            env_file = ".env.test"
        elif not environment:
            raise ValueError(f"ENVIRONMENT must be 'test', 'local', 'staging', or 'production', got empty string")
        else:
            raise ValueError(f"ENVIRONMENT must be 'test', 'local', 'staging', or 'production', got {environment}")

    config = Config()


def get_settings():
    settings = Settings()
    return settings
