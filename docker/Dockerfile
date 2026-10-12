FROM python:3.14-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential pkg-config git \
        libmariadb-dev \
        libmagickwand-dev \
        nodejs npm && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN npm install -g bower less

# Keep the virtualenv outside the bind-mounted source tree
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app
