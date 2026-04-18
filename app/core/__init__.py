"""Core application building blocks and dependencies."""

from app.core.db import SessionDep, get_engine

__all__ = ["SessionDep", "get_engine"]
