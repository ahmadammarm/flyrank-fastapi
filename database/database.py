from typing import List, Dict, Optional
from models.models import Task, TaskCreate, TaskUpdate

# In-memory database
tasks_db: Dict[int, Task] = {}
current_id: int = 1

def get_all_tasks() -> List[Task]:
    return list(tasks_db.values())

def get_task(task_id: int) -> Optional[Task]:
    return tasks_db.get(task_id)

def create_task(task: TaskCreate) -> Task:
    global current_id
    new_task = Task(id=current_id, **task.model_dump())
    tasks_db[current_id] = new_task
    current_id += 1
    return new_task

def update_task(task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    if task_id not in tasks_db:
        return None
    
    stored_task_data = tasks_db[task_id].model_dump()
    update_data = task_update.model_dump(exclude_unset=True)
    updated_task_data = {**stored_task_data, **update_data}
    
    updated_task = Task(**updated_task_data)
    tasks_db[task_id] = updated_task
    return updated_task

def delete_task(task_id: int) -> bool:
    if task_id in tasks_db:
        del tasks_db[task_id]
        return True
    return False
