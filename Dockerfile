# Image de production de l'API.
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Dépendances d'abord : cette couche reste en cache tant que
# pyproject.toml et uv.lock ne changent pas.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY app ./app

RUN useradd --create-home --uid 1000 appuser
USER appuser

ENV ENVIRONMENT=production
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://localhost:{os.getenv(\"PORT\", \"8000\")}/health')"

# PORT est fourni par la plupart des hébergeurs (Render, Railway…).
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers"]
