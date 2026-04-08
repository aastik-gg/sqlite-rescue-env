FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv pip install --system fastapi uvicorn pydantic openai openenv-core

COPY . .

# Explicitly move to the root for the command
CMD ["python", "app.py"]