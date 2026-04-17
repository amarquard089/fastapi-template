ARG PYTHON_VERSION=3.12

# --- Build stage ---
FROM python:${PYTHON_VERSION}-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies first (cached layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

# Copy source and install project
COPY . .
RUN uv sync --locked --no-dev

# --- Runtime stage ---
FROM python:${PYTHON_VERSION}-slim AS runtime

WORKDIR /app

# Copy the virtual environment and source from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80

CMD ["fastapi", "run", "src/main.py", "--port", "80"]
