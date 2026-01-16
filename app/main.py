from fastapi import FastAPI, HTTPException, Depends, status, Query
from sqlmodel import Session
from typing import Optional

from app.database import create_db_and_tables, engine
from app.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    DeleteResponse,
    ErrorResponse
)
from app.crud import (
    create_task,
    get_task_by_id,
    get_all_tasks,
    get_tasks_by_status,
    update_task,
    delete_task,
    delete_all_tasks
)

app = FastAPI(title="Task Management API", version="1.0.0")


@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    create_db_and_tables()


def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get(
    "/tasks",
    response_model=TaskListResponse,
    summary="Get all tasks",
    description="Retrieve all tasks with optional filtering by status and pagination"
)
def get_tasks(
    status: Optional[str] = Query(None, description="Filter tasks by status"),
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    session: Session = Depends(get_session)
):
    """Get all tasks with optional filtering and pagination."""
    if status:
        tasks = get_tasks_by_status(session, status)
    else:
        tasks = get_all_tasks(session, skip=skip, limit=limit)
    
    return TaskListResponse(tasks=tasks, total=len(tasks))


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    description="Retrieve a specific task by its ID",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
def get_task(task_id: int, session: Session = Depends(get_session)):
    """Get a specific task by ID."""
    task = get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with the provided information"
)
def create_new_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    """Create a new task."""
    task = create_task(
        session,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status
    )
    return task


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task by its ID",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session)
):
    """Update an existing task."""
    # Check if at least one field is provided for update
    if not any([task_data.title, task_data.description, task_data.status]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update"
        )
    
    updated_task = update_task(
        session,
        task_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status
    )
    
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return updated_task


@app.delete(
    "/tasks/{task_id}",
    response_model=DeleteResponse,
    summary="Delete a task",
    description="Delete a specific task by its ID",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
def delete_single_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """Delete a specific task by ID."""
    success = delete_task(session, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return DeleteResponse(
        message=f"Task {task_id} deleted successfully",
        deleted_count=1
    )


@app.delete(
    "/tasks",
    response_model=DeleteResponse,
    summary="Delete all tasks",
    description="Delete all tasks from the database"
)
def delete_all(
    session: Session = Depends(get_session)
):
    """Delete all tasks."""
    deleted_count = delete_all_tasks(session)
    return DeleteResponse(
        message=f"All tasks deleted successfully",
        deleted_count=deleted_count
    )
