import sqlite3
import shutil
import os
from typing import Tuple, Dict, Any

from models import RescueAction, RescueObservation, RescueState
from graders import grade_easy_task, grade_medium_task, grade_hard_task

class DatabaseRescueEnv:
    def __init__(self):
        self.task_name = None
        self.steps_taken = 0
        self.working_db = "working.db"
        self.template_dir = "templates"

    def _get_schema(self, cursor: sqlite3.Cursor) -> str:
        """Retrieves the current database schema as a string."""
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        return "\n".join([t[0] for t in tables if t[0] is not None])

    def reset(self, task_name: str) -> RescueObservation:
        """Resets the environment by copying the task's template DB."""
        self.task_name = task_name
        self.steps_taken = 0
        
        # Copy the messy template DB to our working path
        template_path = os.path.join(self.template_dir, f"{task_name}.db")
        if not os.path.exists(template_path):
            raise ValueError(f"Template DB for task '{task_name}' not found.")
            
        shutil.copyfile(template_path, self.working_db)
        
        # Return initial observation
        with sqlite3.connect(self.working_db) as conn:
            schema = self._get_schema(conn.cursor())
            
        return RescueObservation(
            schema_info=schema,
            query_result=None,
            rows_affected=0,
            error=None
        )

    def step(self, action: RescueAction) -> Tuple[RescueObservation, float, bool, Dict[str, Any]]:
        self.steps_taken += 1
        reward = 0.0
        done = False
        info = {}

        # If the agent submits, trigger the grader and end the episode
        if action.submit:
            reward = self._grade_task()
            done = True
            with sqlite3.connect(self.working_db) as conn:
                schema = self._get_schema(conn.cursor())
            return RescueObservation(schema_info=schema), reward, done, info

        # Otherwise, execute the query
        obs = RescueObservation(schema_info="", rows_affected=0)
        
        try:
            with sqlite3.connect(self.working_db) as conn:
                conn.row_factory = sqlite3.Row 
                cursor = conn.cursor()
                
                cursor.execute(action.query)
                conn.commit()
                
                obs.schema_info = self._get_schema(cursor)
                obs.rows_affected = cursor.rowcount
                
                # If it was a SELECT query, fetch results
                if action.query.strip().upper().startswith("SELECT"):
                    rows = cursor.fetchmany(50) # Limit to avoid context bloat
                    obs.query_result = [dict(row) for row in rows]
                    
        except sqlite3.Error as e:
            obs.error = str(e)
            
        return obs, reward, done, info

    def state(self) -> RescueState:
        return RescueState(
            task_name=self.task_name,
            steps_taken=self.steps_taken,
            db_path=self.working_db
        )
        
    def _grade_task(self) -> float:
        """Routes the current database to the correct scoring logic."""
        if self.task_name == "easy_data_cleaning":
            return grade_easy_task(self.working_db)
        elif self.task_name == "medium_schema_normalization":
            return grade_medium_task(self.working_db)
        elif self.task_name == "hard_complex_reconciliation":
            return grade_hard_task(self.working_db)
        return 0.0