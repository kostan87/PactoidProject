FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project

COPY . .
RUN uv sync

CMD ["bash", "-c", "\
  mkdir -p /root/.ssh-local && \
  cp /root/.ssh/id_ed25519 /root/.ssh-local/ 2>/dev/null; \
  cp /root/.ssh/id_ed25519.pub /root/.ssh-local/ 2>/dev/null; \
  chmod 700 /root/.ssh-local; \
  chmod 600 /root/.ssh-local/id_ed25519 2>/dev/null; \
  chmod 644 /root/.ssh-local/id_ed25519.pub 2>/dev/null; \
  sleep infinity \
"]