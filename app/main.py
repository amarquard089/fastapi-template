"""Entry point for the application."""

from fastapi import FastAPI
from fastapi.responses import Response

from app.api import api_router
from app.settings import settings

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
    return {"status": "ok"}


@app.options("/health")
async def health_options():
    """Health options endpoint."""
    return Response(status_code=204)
