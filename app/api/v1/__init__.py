# app/api/v1/__init__.py
from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

api_router = APIRouter()

# Try to import routers and include them. If an import raises, we log it (so app still starts)
try:
    # these modules should define a variable `router` (FastAPI APIRouter)
    from .routers import users_router, tasks_router, projects_router  # type: ignore

    api_router.include_router(users_router.router, prefix="/users", tags=["users"])
    api_router.include_router(tasks_router.router, prefix="/tasks", tags=["tasks"])
    api_router.include_router(projects_router.router, prefix="/projects", tags=["projects"])

except Exception as exc:  # catch import-time errors and log them
    logger.exception("Failed to import or register v1 routers: %s", exc)
    # Optionally, re-raise here if you prefer startup to fail hard:
    # raise
