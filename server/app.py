import uvicorn
from fastapi import FastAPI
import sys
import os

# Ensure the root directory is in the path so we can import env.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env import DatabaseRescueEnv

# OpenEnv looks for an ASGI 'app' object
app = FastAPI(title="SQLite Rescue Environment API")
env_instance = DatabaseRescueEnv()

@app.get("/")
def health_check():
    """Satisfies the HF Space health check ping (must return 200)."""
    return {"status": "ok", "environment": "sqlite-rescue-env"}

@app.post("/reset")
def reset_env(task_name: str = "easy_data_cleaning"):
    """Satisfies the pre-submission HF Space ping for reset()."""
    obs = env_instance.reset(task_name)
    return {"status": "reset", "observation": obs.dict()}

def main():
    """The entry point referenced in pyproject.toml."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()