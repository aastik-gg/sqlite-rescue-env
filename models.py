from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class RescueAction(BaseModel):
    query: str = Field(description="The SQL query to execute against the SQLite database.")
    submit: bool = Field(default=False, description="Set to True ONLY when you have completed the task and are ready for grading.")

class RescueObservation(BaseModel):
    schema_info: str = Field(description="The current schema of the database.")
    query_result: Optional[List[Dict[str, Any]]] = Field(default=None, description="Results from a SELECT query, limited to 50 rows.")
    rows_affected: int = Field(default=0, description="Number of rows modified by INSERT/UPDATE/DELETE.")
    error: Optional[str] = Field(default=None, description="SQL execution error message, if any.")

class RescueState(BaseModel):
    task_name: str
    steps_taken: int
    db_path: str