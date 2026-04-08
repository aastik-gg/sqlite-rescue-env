import uvicorn
from fastapi import FastAPI
import sys
import os

# Force the root directory into the python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from env import DatabaseRescueEnv

app = FastAPI(title="SQLite Rescue Environment API")
env_instance = DatabaseRescueEnv()

@app.get("/")
def health_check():
    return {"status": "ok", "environment": "sqlite-rescue-env"}

@app.post("/reset")
def reset_env(task_name: str = "easy_data_cleaning"):
    obs = env_instance.reset(task_name)
    return {"status": "reset", "observation": obs.model_dump()} # Changed .dict() to .model_dump() for Pydantic v2

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860) # Port 7860 is the HF default

if __name__ == "__main__":
    main()