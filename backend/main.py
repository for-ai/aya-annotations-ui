import logging
import os
import sys

from pathlib import Path

from alembic.config import Config as AlembicConfig
from alembic.command import upgrade as alembic_upgrade

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from instruct_multilingual.api.v1.api import api_router
from instruct_multilingual.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        settings.for_ai_url,
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# https://fastapi.tiangolo.com/advanced/events/
if settings.run_migrations_on_startup:
    @app.on_event("startup")
    def run_alembic_migrations():
        alembic_ini_path = (
            Path(__file__).parent / "alembic.ini"
        ).as_posix()

        alembic_cfg = AlembicConfig(
            str(alembic_ini_path),
            attributes={'configure_logger': False},
        )

        logger.info("attempting to run alembic migrations on startup...")
        try:
            alembic_upgrade(alembic_cfg, "head")
        except Exception:
            logger.exception("alembic migrations failed on startup due to exception")
        else:
            logger.info("successfully upgraded alembic!")


app.include_router(api_router, prefix="/api/v1")
            
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
):
    logger.error(f"Request validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.exception_handler(HTTPException)
async def internal_server_error_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error(f"Internal server error: {exc.detail}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}
