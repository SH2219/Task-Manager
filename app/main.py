# app/main.py
import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging_config import configure_logging
from app.core.config import settings
from app.api.v1 import api_router  # api_router from app/api/v1/__init__.py

# configure logging early
configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)

# CORS - adjust origins as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else [],  # in prod, set real domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(api_router, prefix="/api/v1")

# health endpoint
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# startup/shutdown hooks (optional)
@app.on_event("startup")
async def on_startup():
    logger.info("Starting app: %s", settings.APP_NAME)
    # e.g., warm caches, connect to external services, run migrations check etc.

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down app")
    # e.g., close connections if needed
