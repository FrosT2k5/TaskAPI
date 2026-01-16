#!/usr/bin/env python3
"""
Test script to demonstrate CRUD operations on the Task database.
This script will create the database, perform various CRUD operations,
and print results to verify functionality.
"""

from sqlmodel import Session
from app.database import create_db_and_tables, engine
from app.crud import (
    create_task,
    get_task_by_id,
    get_all_tasks,
    get_tasks_by_status,
    update_task,
    delete_task,
    delete_all_tasks
)


def print_separator(title: str):
    """Print a formatted separator."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_task(task, prefix: str = ""):
    """Print task details."""
    if task:
        print(f"{prefix}Task ID: {task.id}")
        print(f"{prefix}Title: {task.title}")
        print(f"{prefix}Description: {task.description}")
        print(f"{prefix}Status: {task.status}")
        print(f"{prefix}Created At: {task.created_at}")
        print(f"{prefix}Updated At: {task.updated_at}")
    else:
        print(f"{prefix}Task not found")


def print_tasks_list(tasks, title: str = "Tasks"):
    """Print a list of tasks."""
    print(f"\n{title} (Total: {len(tasks)}):")
    if not tasks:
        print("  No tasks found")
    else:
        for task in tasks:
            print(f"  - [ID: {task.id}] {task.title} (Status: {task.status})")


def main():
    print_separator("DATABASE INITIALIZATION")
    print("Creating database and tables...")
    create_db_and_tables()
    print("✓ Database created successfully!")

    with Session(engine) as session:
        # Clean up any existing data
        print_separator("CLEANUP")
        deleted_count = delete_all_tasks(session)
        print(f"Cleared {deleted_count} existing tasks from database")

        # CREATE operations
        print_separator("CREATE OPERATIONS")
        print("\nCreating multiple tasks...")
        
        task1 = create_task(
            session,
            title="Implement user authentication",
            description="Add JWT-based authentication to the API",
            status="in_progress"
        )
        print(f"\n✓ Created task 1:")
        print_task(task1, "  ")

        task2 = create_task(
            session,
            title="Write unit tests",
            description="Add comprehensive unit tests for all endpoints",
            status="pending"
        )
        print(f"\n✓ Created task 2:")
        print_task(task2, "  ")

        task3 = create_task(
            session,
            title="Setup CI/CD pipeline",
            description="Configure GitHub Actions for automated testing and deployment",
            status="pending"
        )
        print(f"\n✓ Created task 3:")
        print_task(task3, "  ")

        task4 = create_task(
            session,
            title="Update documentation",
            description="Document all API endpoints and usage examples",
            status="in_progress"
        )
        print(f"\n✓ Created task 4:")
        print_task(task4, "  ")

        task5 = create_task(
            session,
            title="Fix login bug",
            description="Resolve issue with password validation",
            status="completed"
        )
        print(f"\n✓ Created task 5:")
        print_task(task5, "  ")

        # READ operations
        print_separator("READ OPERATIONS")
        
        # Get all tasks
        all_tasks = get_all_tasks(session)
        print_tasks_list(all_tasks, "All Tasks in Database")

        # Get task by ID
        print(f"\n\nRetrieving task with ID {task2.id}:")
        retrieved_task = get_task_by_id(session, task2.id)
        print_task(retrieved_task, "  ")

        # Get tasks by status
        pending_tasks = get_tasks_by_status(session, "pending")
        print_tasks_list(pending_tasks, "\nPending Tasks")

        in_progress_tasks = get_tasks_by_status(session, "in_progress")
        print_tasks_list(in_progress_tasks, "\nIn Progress Tasks")

        completed_tasks = get_tasks_by_status(session, "completed")
        print_tasks_list(completed_tasks, "\nCompleted Tasks")

        # UPDATE operations
        print_separator("UPDATE OPERATIONS")
        
        # Update task 2 (change status)
        print(f"\nUpdating task {task2.id}...")
        print("BEFORE UPDATE:")
        print_task(task2, "  ")
        
        updated_task = update_task(
            session,
            task2.id,
            status="in_progress"
        )
        print("\nAFTER UPDATE:")
        print_task(updated_task, "  ")

        # Update task 3 (change title and description)
        print(f"\n\nUpdating task {task3.id}...")
        print("BEFORE UPDATE:")
        before_update = get_task_by_id(session, task3.id)
        print_task(before_update, "  ")
        
        updated_task2 = update_task(
            session,
            task3.id,
            title="Setup CI/CD with Docker",
            description="Configure GitHub Actions with Docker containerization",
            status="in_progress"
        )
        print("\nAFTER UPDATE:")
        print_task(updated_task2, "  ")

        # Update task 4 (mark as completed)
        print(f"\n\nMarking task {task4.id} as completed...")
        print("BEFORE UPDATE:")
        before_completion = get_task_by_id(session, task4.id)
        print_task(before_completion, "  ")
        
        completed_task = update_task(session, task4.id, status="completed")
        print("\nAFTER UPDATE:")
        print_task(completed_task, "  ")

        # Show updated task list
        print("\n\nAll tasks after updates:")
        all_tasks_after_update = get_all_tasks(session)
        print_tasks_list(all_tasks_after_update, "Updated Task List")

        # DELETE operations
        print_separator("DELETE OPERATIONS")
        
        # Delete task 1
        print(f"\nDeleting task {task1.id}...")
        print("Task BEFORE deletion:")
        task_to_delete = get_task_by_id(session, task1.id)
        print_task(task_to_delete, "  ")
        
        delete_result = delete_task(session, task1.id)
        print(f"\nDeletion result: {'✓ Success' if delete_result else '✗ Failed'}")
        
        print("\nVerifying deletion - trying to retrieve deleted task:")
        deleted_task_check = get_task_by_id(session, task1.id)
        print_task(deleted_task_check, "  ")

        # Delete task 5
        print(f"\n\nDeleting task {task5.id}...")
        delete_result2 = delete_task(session, task5.id)
        print(f"Deletion result: {'✓ Success' if delete_result2 else '✗ Failed'}")

        # Show final task list
        print("\n\nFinal task list after deletions:")
        final_tasks = get_all_tasks(session)
        print_tasks_list(final_tasks, "Remaining Tasks")

        # Summary
        print_separator("SUMMARY")
        print(f"✓ Created: 5 tasks")
        print(f"✓ Updated: 3 tasks")
        print(f"✓ Deleted: 2 tasks")
        print(f"✓ Remaining: {len(final_tasks)} tasks")
        print("\nFinal task breakdown by status:")
        for status in ["pending", "in_progress", "completed"]:
            tasks_by_status = get_tasks_by_status(session, status)
            print(f"  - {status.capitalize()}: {len(tasks_by_status)}")

        print("\n" + "=" * 70)
        print("  CRUD operations completed successfully!")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
