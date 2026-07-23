from fastapi import APIRouter, HTTPException, status, Depends, Query
import sqlite3
from typing import List, Optional

from models import schemas
from database.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[schemas.Task])
async def read_tasks(
    db: sqlite3.Connection = Depends(get_db),
    search: Optional[str] = Query(None, description="Search term for title or description"),
    sort_by: Optional[str] = Query(None, description="Sort by 'title' or 'completed'"),
    sort_order: Optional[str] = Query("asc", description="Sort order: 'asc' or 'desc'")
):
    query = "SELECT * FROM tasks"
    params = []
    
    # Search Filter
    if search:
        query += " WHERE title LIKE ? OR description LIKE ?"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])
    
    # Sort Filter
    valid_sort_columns = {"id", "title", "completed"}
    sort_column = "id"
    if sort_by and sort_by in valid_sort_columns:
        sort_column = sort_by
        
    order = "DESC" if sort_order.lower() == "desc" else "ASC"
    
    query += f" ORDER BY {sort_column} {order}"
    
    cursor = db.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # Convert sqlite3.Row to dict for pydantic
    return [dict(row) for row in rows]

@router.get("/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return dict(row)

@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: schemas.TaskCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
        (task.title, task.description, task.completed)
    )
    db.commit()
    task_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    return dict(row)

@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task_update: schemas.TaskUpdate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        return dict(row)
        
    set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
    params = list(update_data.values())
    params.append(task_id)
    
    cursor.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", params)
    db.commit()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated_row = cursor.fetchone()
    return dict(updated_row)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return None
