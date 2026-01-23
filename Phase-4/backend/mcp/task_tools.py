"""
MCP (Model Context Protocol) tools for task operations.
These tools will be exposed to the Cohere AI agent via MCP.
"""

import asyncio
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from datetime import datetime, timezone
from models import Task, TaskCreate, TaskUpdate, User
from database import get_session
from auth import get_current_user_id_from_token


class TaskInput(BaseModel):
    """Input model for task operations."""
    title: str = Field(description="The title of the task")
    description: Optional[str] = Field(default="", description="The description of the task")


class UpdateTaskInput(BaseModel):
    """Input model for updating tasks."""
    task_id: int = Field(description="The ID of the task to update")
    title: Optional[str] = Field(default=None, description="The new title of the task")
    description: Optional[str] = Field(default=None, description="The new description of the task")
    is_completed: Optional[bool] = Field(default=None, description="Whether the task is completed")


class ToggleCompleteInput(BaseModel):
    """Input model for toggling task completion."""
    task_id: int = Field(description="The ID of the task to toggle")


class DeleteTaskInput(BaseModel):
    """Input model for deleting tasks."""
    task_id: int = Field(description="The ID of the task to delete")


class GetTasksInput(BaseModel):
    """Input model for getting tasks."""
    status: Optional[str] = Field(default=None, description="Filter by status: 'all', 'completed', 'pending'")


async def add_task_tool(title: str, description: str = "", token: str = None) -> Dict:
    """
    Add a new task to the user's list.

    Args:
        title: The title of the task
        description: The description of the task
        token: JWT token for authentication

    Returns:
        Dict containing the result of the operation
    """
    if not token:
        return {"error": "Authentication token is required"}

    try:
        # Verify user from token
        user_id = get_current_user_id_from_token(token)
        if not user_id:
            return {"error": "Invalid or expired token"}

        # Create database session
        with next(get_session()) as session:
            # Ensure user exists in our DB (Lazy upsert)
            user = session.get(User, user_id)
            if not user:
                user = User(id=user_id, email=f"{user_id}@placeholder.com")
                session.add(user)
                session.flush()

            # Create the task
            task_create = TaskCreate(title=title, description=description)
            task_data = task_create.model_dump()
            db_task = Task(**task_data, owner_id=user_id)
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Return task data in the same format as the API
            return {
                "success": True,
                "message": f"Task '{db_task.title}' added successfully",
                "task_id": db_task.id,
                "task_title": db_task.title,
                "task": {
                    "id": db_task.id,
                    "title": db_task.title,
                    "description": db_task.description,
                    "is_completed": db_task.is_completed,
                    "created_at": db_task.created_at.isoformat() if db_task.created_at else None,
                    "updated_at": db_task.updated_at.isoformat() if db_task.updated_at else None,
                    "owner_id": db_task.owner_id
                }
            }
    except Exception as e:
        return {"error": f"Failed to add task: {str(e)}"}


async def get_tasks_tool(status: Optional[str] = None, token: str = None) -> Dict:
    """
    Retrieve the user's tasks.

    Args:
        status: Filter by status ('completed', 'pending', 'all'). Default is 'all'.
        token: JWT token for authentication

    Returns:
        Dict containing the list of tasks
    """
    if not token:
        return {"error": "Authentication token is required"}

    try:
        # Verify user from token
        user_id = get_current_user_id_from_token(token)
        if not user_id:
            return {"error": "Invalid or expired token"}

        # Create database session
        with next(get_session()) as session:
            # Query tasks based on user ID and optional status filter
            query = select(Task).where(Task.owner_id == user_id)

            if status == "completed":
                query = query.where(Task.is_completed == True)
            elif status == "pending":
                query = query.where(Task.is_completed == False)

            tasks = session.exec(query).all()

            # Format tasks for AI consumption
            formatted_tasks = []
            for task in tasks:
                formatted_tasks.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_completed": task.is_completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                    "owner_id": task.owner_id
                })

            return {
                "success": True,
                "tasks": formatted_tasks,
                "count": len(formatted_tasks)
            }
    except Exception as e:
        return {"error": f"Failed to retrieve tasks: {str(e)}"}


async def update_task_tool(task_id: int = None, title_to_find: str = None, new_title: str = None, description: str = None, token: str = None) -> Dict:
    """
    Update an existing task.

    Args:
        task_id: The ID of the task to update (optional if title_to_find is provided)
        title_to_find: The title of the task to find (optional if task_id is provided)
        new_title: New title (optional)
        description: New description (optional)
        token: JWT token for authentication

    Returns:
        Dict containing the result of the operation
    """
    if not token:
        return {"error": "Authentication token is required"}

    if task_id is None and title_to_find is None:
        return {"error": "Either task_id or title_to_find must be provided"}

    try:
        # Verify user from token
        user_id = get_current_user_id_from_token(token)
        if not user_id:
            return {"error": "Invalid or expired token"}

        # Create database session
        with next(get_session()) as session:
            # Get the task - either by ID or by title
            db_task = None
            if task_id:
                db_task = session.get(Task, task_id)
            else:
                # Search for task by title
                stmt = select(Task).where(Task.owner_id == user_id, Task.title == title_to_find)
                result = session.exec(stmt)
                db_task = result.first()

            if not db_task:
                return {"error": "Task not found"}

            # Verify user owns the task
            if db_task.owner_id != user_id:
                return {"error": "Not authorized to update this task"}

            # Prepare update data
            update_data = {}
            if new_title is not None:
                update_data["title"] = new_title
            if description is not None:
                update_data["description"] = description

            if update_data:
                # Update the task
                for key, value in update_data.items():
                    setattr(db_task, key, value)

                db_task.updated_at = datetime.now(timezone.utc)
                session.add(db_task)
                session.commit()
                session.refresh(db_task)

                # Return updated task data in the same format as the API
                return {
                    "success": True,
                    "message": f"Task '{db_task.title}' updated successfully",
                    "task_id": db_task.id,
                    "task": {
                        "id": db_task.id,
                        "title": db_task.title,
                        "description": db_task.description,
                        "is_completed": db_task.is_completed,
                        "created_at": db_task.created_at.isoformat() if db_task.created_at else None,
                        "updated_at": db_task.updated_at.isoformat() if db_task.updated_at else None,
                        "owner_id": db_task.owner_id
                    }
                }
            else:
                # Return task data in the same format as the API
                return {
                    "success": True,
                    "message": "No changes made to the task",
                    "task_id": db_task.id,
                    "task": {
                        "id": db_task.id,
                        "title": db_task.title,
                        "description": db_task.description,
                        "is_completed": db_task.is_completed,
                        "created_at": db_task.created_at.isoformat() if db_task.created_at else None,
                        "updated_at": db_task.updated_at.isoformat() if db_task.updated_at else None,
                        "owner_id": db_task.owner_id
                    }
                }
    except Exception as e:
        return {"error": f"Failed to update task: {str(e)}"}


async def delete_task_tool(task_id: int = None, title_to_delete: str = None, token: str = None) -> Dict:
    """
    Delete a task.

    Args:
        task_id: The ID of the task to delete (optional if title_to_delete is provided)
        title_to_delete: The title of the task to delete (optional if task_id is provided)
        token: JWT token for authentication

    Returns:
        Dict containing the result of the operation
    """
    if not token:
        return {"error": "Authentication token is required"}

    if task_id is None and title_to_delete is None:
        return {"error": "Either task_id or title_to_delete must be provided"}

    try:
        # Verify user from token
        user_id = get_current_user_id_from_token(token)
        if not user_id:
            return {"error": "Invalid or expired token"}

        # Create database session
        with next(get_session()) as session:
            # Get the task - either by ID or by title
            db_task = None
            if task_id:
                db_task = session.get(Task, task_id)
            else:
                # Search for task by title
                stmt = select(Task).where(Task.owner_id == user_id, Task.title == title_to_delete)
                result = session.exec(stmt)
                db_task = result.first()

            if not db_task:
                return {"error": "Task not found"}

            # Verify user owns the task
            if db_task.owner_id != user_id:
                return {"error": "Not authorized to delete this task"}

            # Store task info before deletion for the response
            task_info = {
                "id": db_task.id,
                "title": db_task.title,
                "description": db_task.description,
                "is_completed": db_task.is_completed,
                "created_at": db_task.created_at.isoformat() if db_task.created_at else None,
                "updated_at": db_task.updated_at.isoformat() if db_task.updated_at else None,
                "owner_id": db_task.owner_id
            }

            # Delete the task
            session.delete(db_task)
            session.commit()

            return {
                "success": True,
                "message": f"Task '{db_task.title}' deleted successfully",
                "deleted_task": task_info
            }
    except Exception as e:
        return {"error": f"Failed to delete task: {str(e)}"}


async def mark_complete_tool(task_id: int = None, title_to_mark: str = None, token: str = None) -> Dict:
    """
    Toggle the completion status of a task.

    Args:
        task_id: The ID of the task to toggle (optional if title_to_mark is provided)
        title_to_mark: The title of the task to mark (optional if task_id is provided)
        token: JWT token for authentication

    Returns:
        Dict containing the result of the operation
    """
    if not token:
        return {"error": "Authentication token is required"}

    if task_id is None and title_to_mark is None:
        return {"error": "Either task_id or title_to_mark must be provided"}

    try:
        # Verify user from token
        user_id = get_current_user_id_from_token(token)
        if not user_id:
            return {"error": "Invalid or expired token"}

        # Create database session
        with next(get_session()) as session:
            # Get the task - either by ID or by title
            db_task = None
            if task_id:
                db_task = session.get(Task, task_id)
            else:
                # Search for task by title
                stmt = select(Task).where(Task.owner_id == user_id, Task.title == title_to_mark)
                result = session.exec(stmt)
                db_task = result.first()

            if not db_task:
                return {"error": "Task not found"}

            # Verify user owns the task
            if db_task.owner_id != user_id:
                return {"error": "Not authorized to modify this task"}

            # Toggle completion status
            new_status = not db_task.is_completed
            db_task.is_completed = new_status
            db_task.updated_at = datetime.now(timezone.utc)
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            status_text = "completed" if new_status else "marked as pending"

            # Return updated task data in the same format as the API
            return {
                "success": True,
                "message": f"Task '{db_task.title}' {status_text}",
                "task_id": db_task.id,
                "is_completed": new_status,
                "task": {
                    "id": db_task.id,
                    "title": db_task.title,
                    "description": db_task.description,
                    "is_completed": db_task.is_completed,
                    "created_at": db_task.created_at.isoformat() if db_task.created_at else None,
                    "updated_at": db_task.updated_at.isoformat() if db_task.updated_at else None,
                    "owner_id": db_task.owner_id
                }
            }
    except Exception as e:
        return {"error": f"Failed to toggle task completion: {str(e)}"}