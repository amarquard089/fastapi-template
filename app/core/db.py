"""Database connection and session management."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.settings import settings

engine = create_async_engine(settings.db.async_url, echo=settings.debug)  # echo for logging SQL queries


async def get_engine() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session.

    Returns:
        AsyncGenerator[AsyncSession, None]: An async generator yielding a database session.

    Yields:
        Iterator[AsyncGenerator[AsyncSession, None]]: An async generator yielding a database session.

    """
    async with AsyncSession(engine) as sess:
        yield sess


SessionDep = Annotated[AsyncSession, Depends(get_engine)]
"""Dependency for getting a database session.

Usage:
```python
from src.core import SessionDep
from fastapi import APIRouter

router = APIRouter()

@router.get("/some-endpoint")
async def some_endpoint(db: SessionDep):
    # Use the db session here
```
"""
