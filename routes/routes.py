from fastapi import APIRouter, HTTPException, status
from typing import List
from models.models import Task, TaskCreate, TaskUpdate
from database import database as db

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[Task])
async def read_tasks():
    return db.get_all_tasks()

@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    return db.create_task(task)

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    updated_task = db.update_task(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    success = db.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
