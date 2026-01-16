from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime, UTC
from app.models import Task


def create_task(session: Session, title: str, description: Optional[str] = None, status: str = "pending") -> Task:
    """Create a new task in the database."""
    task = Task(title=title, description=description, status=status)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task_by_id(session: Session, task_id: int) -> Optional[Task]:
    """Retrieve a task by its ID."""
    return session.get(Task, task_id)


def get_all_tasks(session: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    """Retrieve all tasks with pagination."""
    statement = select(Task).offset(skip).limit(limit)
    results = session.exec(statement)
    return list(results.all())


def get_tasks_by_status(session: Session, status: str) -> List[Task]:
    """Retrieve tasks filtered by status."""
    statement = select(Task).where(Task.status == status)
    results = session.exec(statement)
    return list(results.all())


def update_task(
    session: Session,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None
) -> Optional[Task]:
    """Update an existing task."""
    task = session.get(Task, task_id)
    if not task:
        return None
    
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if status is not None:
        task.status = status
    
    task.updated_at = datetime.now(UTC)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int) -> bool:
    """Delete a task by its ID."""
    task = session.get(Task, task_id)
    if not task:
        return False
    
    session.delete(task)
    session.commit()
    return True


def delete_all_tasks(session: Session) -> int:
    """Delete all tasks from the database. Returns count of deleted tasks."""
    statement = select(Task)
    results = session.exec(statement)
    tasks = results.all()
    count = len(tasks)
    
    for task in tasks:
        session.delete(task)
    
    session.commit()
    return count
