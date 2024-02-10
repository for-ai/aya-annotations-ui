# https://fastapi.tiangolo.com/tutorial/bigger-applications/
from fastapi import APIRouter

from instruct_multilingual.api.v1 import (
    leaderboards,
    tasks,
    users,
    auth,
    auth_discord,
    auth_google,
)

api_router = APIRouter()

api_router.include_router(leaderboards.router, prefix="/leaderboards", tags=["leaderboards"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(auth_discord.router, prefix="/auth/discord", tags=["auth"])
api_router.include_router(auth_google.router, prefix="/auth/google", tags=["auth"])
