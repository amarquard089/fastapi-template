"""Global pytest bootstrap configuration."""

import os

os.environ.setdefault("FASTAPI_TEMPLATE__ENV_FILE", ".env.testing")
