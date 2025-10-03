# app/core/logging_config.py
import logging
import sys
from typing import Dict
from logging.config import dictConfig

from .config import settings


DEFAULT_LOG_LEVEL = "DEBUG" if settings.DEBUG else "INFO"


def configure_logging() -> None:
    """
    Configure basic console logging. Call this early in app startup
    (e.g., in app/main.py before creating the FastAPI app).
    """
    log_config: Dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout,
            }
        },
        "root": {
            "handlers": ["console"],
            "level": DEFAULT_LOG_LEVEL,
        },
        "loggers": {
            # uvicorn (ASGI server)
            "uvicorn": {"handlers": ["console"], "level": DEFAULT_LOG_LEVEL, "propagate": False},
            "uvicorn.error": {"handlers": ["console"], "level": DEFAULT_LOG_LEVEL, "propagate": False},
            "uvicorn.access": {"handlers": ["console"], "level": "INFO", "propagate": False},
            # SQLAlchemy engine (too noisy sometimes)
            "sqlalchemy.engine": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        },
    }

    dictConfig(log_config)
    logging.getLogger("app").debug("Logging configured. Level=%s", DEFAULT_LOG_LEVEL)
