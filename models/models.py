from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., title="Task Title", min_length=1)
    description: Optional[str] = Field(None, title="Task Description")
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = Field(None, title="Task Title", min_length=1)

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True