import pytest
from app.core.db import get_engine


@pytest.mark.asyncio
async def test_get_engine_yields_session():
    """Test that get_engine yields an AsyncSession."""
    gen = get_engine()
    session = await gen.asend(None)

    assert session is not None
