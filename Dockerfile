# Use a lightweight python image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into the system path so they are always findable
RUN uv pip install --system fastapi uvicorn pydantic openai openenv-core

# Copy the rest of the code
COPY . .

# Set PYTHONPATH to the current directory so imports always work
ENV PYTHONPATH=/app

# Start the server directly
CMD ["python", "server/app.py"]