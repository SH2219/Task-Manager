# app/api/__init__.py
"""
Top-level API package: re-export the v1 router.
So other modules can do: `from app.api import api_router`
"""
from .v1 import api_router

__all__ = ["api_router"]
