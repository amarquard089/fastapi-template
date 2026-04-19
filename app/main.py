"""Entry point for the application."""

import logging

from fastapi import FastAPI
from fastapi.responses import Response

from app.api import api_router
from app.logging import configure_logging
from app.settings import settings

configure_logging(settings.log_level)

logger = logging.getLogger(__name__)

app = FastAPI(
    debug=settings.debug,
    title=settings.app.title,
    summary=settings.app.summary,
    description=settings.app.description,
    version=settings.app.version,
)

app.include_router(api_router)


@app.get("/health")
async def health():
    """Health endpoint."""
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@app.options("/health")
async def health_options():
    """Health options endpoint."""
    logger.info("Health options endpoint called")
    return Response(status_code=204)
