# Use a lightweight python image
FROM python:3.11-slim

# Install system dependencies (SQLite is built-in, but we need curl for healthchecks)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv (the fast python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy the dependency files first to cache the layer
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the rest of the application code
COPY . .

# Expose the port the FastAPI server runs on
EXPOSE 8000

# Start the OpenEnv server
CMD ["uv", "run", "server/app.py"]