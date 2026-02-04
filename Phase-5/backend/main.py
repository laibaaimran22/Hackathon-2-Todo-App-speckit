from fastapi import FastAPI, Depends, HTTPException, status, Security, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from sqlalchemy import text
from typing import List, Optional
import logging

# Import Dapr integration
from dapr_integration import dapr_client
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from pydantic import BaseModel
from jose import jwt
import secrets

from database import engine, get_session, init_db
from models import Task, TaskCreate, TaskRead, TaskUpdate, User, Tag, TaskTagLink
from auth import get_current_user_id
# Import local MCP server to avoid conflicts with system mcp package
import importlib.util
import os

# Load the local mcp server module directly to avoid naming conflicts
mcp_server_path = os.path.join(os.path.dirname(__file__), 'mcp', 'server.py')
spec = importlib.util.spec_from_file_location("local_mcp_server", mcp_server_path)
local_mcp_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(local_mcp_module)
mcp_app = local_mcp_module.app

load_dotenv()

# Configure app for Hugging Face Spaces
app = FastAPI(
    title="Todo Evolution API",
    description="Phase 2 Backend: Authenticated REST API for Todo Management",
    version="1.0.0",
    # Add root_path for reverse proxy (like Hugging Face Spaces)
    root_path=""  # Hugging Face Spaces should handle routing automatically
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Log validation details to help debug 422s from the frontend
    print("[VALIDATION ERROR]", exc.errors())
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors()})

# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()
    # Initialize Dapr client
    try:
        dapr_client.initialize()
        print("[DAPR] Dapr client initialized successfully")
    except Exception as e:
        print(f"[DAPR] Failed to initialize Dapr client: {e}")
        print("[DAPR] Continuing without Dapr integration")

# CORS Configuration - Split comma-separated string into list
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]
print(f"[CORS] Configured CORS origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Now a proper list
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Mount MCP server under /mcp path
app.mount("/mcp", mcp_app)

class AuthRequest(BaseModel):
    email: str
    password: str

@app.post("/api/auth/sign-in/email")
async def sign_in_email(request: AuthRequest):
    # Simulate authentication - in a real app, you'd verify credentials
    # For demo purposes, we'll generate a JWT token
    # Get the shared secret using the same logic as auth.py to handle multiple possible environment variable names
    secret = (
        os.getenv("BETTER_AUTH_SECRET") or
        os.getenv("better_auth_secret") or  # lowercase variant
        os.getenv("JWT_SECRET") or
        os.getenv("jwt_secret")  # lowercase variant
    )
    if not secret:
        raise HTTPException(status_code=500, detail="Auth secret not configured")

    # Create a simple JWT token with user info
    token_data = {
        "sub": f"user_{secrets.token_hex(8)}",  # Unique user ID
        "email": request.email,
        "exp": datetime.now(timezone.utc).timestamp() + 86400 * 7,  # 7 days expiry
        "iat": datetime.now(timezone.utc).timestamp()
    }

    token = jwt.encode(token_data, secret, algorithm="HS256")

    return {
        "session": {
            "token": token,
            "expiresAt": datetime.now(timezone.utc).timestamp() + 86400 * 7
        },
        "user": {
            "id": token_data["sub"],
            "email": request.email
        }
    }

@app.post("/api/auth/sign-up/email")
async def sign_up_email(request: AuthRequest):
    # For simplicity, treat sign up same as sign in
    # Get the shared secret using the same logic as auth.py to handle multiple possible environment variable names
    secret = (
        os.getenv("BETTER_AUTH_SECRET") or
        os.getenv("better_auth_secret") or  # lowercase variant
        os.getenv("JWT_SECRET") or
        os.getenv("jwt_secret")  # lowercase variant
    )
    if not secret:
        raise HTTPException(status_code=500, detail="Auth secret not configured")

    token_data = {
        "sub": f"user_{secrets.token_hex(8)}",  # Unique user ID
        "email": request.email,
        "exp": datetime.now(timezone.utc).timestamp() + 86400 * 7,  # 7 days expiry
        "iat": datetime.now(timezone.utc).timestamp()
    }

    token = jwt.encode(token_data, secret, algorithm="HS256")

    return {
        "session": {
            "token": token,
            "expiresAt": datetime.now(timezone.utc).timestamp() + 86400 * 7
        },
        "user": {
            "id": token_data["sub"],
            "email": request.email
        }
    }

@app.post("/api/auth/sign-out")
async def sign_out():
    return {"success": True}

@app.get("/api/auth/user")
async def get_user_raw(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    # Import here to avoid circular imports
    from auth import get_current_user_data

    user_id, email = get_current_user_data(credentials)
    return {
        "id": user_id,
        "email": email
    }

@app.get("/")
async def root():
    return {
        "message": "Todo Evolution Backend API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "auth": "/api/auth",
            "tasks": "/api/tasks",
            "mcp": "/mcp/"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Task Endpoints
@app.post("/api/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    session: Session = Depends(get_session),
    task_in: TaskCreate,
    current_user_id: str = Depends(get_current_user_id)
):
    try:
        print(f"[TASK] Creating task for user: {current_user_id}, task_data: {task_in.model_dump()}")
        # Ensure user exists in our DB (Lazy upsert)
        user = session.get(User, current_user_id)
        if not user:
            # We need to get the email from the JWT token to create a proper user
            # Since we can't easily access the JWT payload here, we'll create with a placeholder
            # In a real implementation, you'd want to pass the email from authentication
            user = User(id=current_user_id, email=f"{current_user_id}@example.com")
            session.add(user)
            print(f"[TASK] Created new user: {current_user_id}")

        # Extract tag names before creating the task
        tag_names = getattr(task_in, 'tag_names', [])

        # Prepare task data excluding tag_names
        task_data = task_in.model_dump()
        task_data.pop('tag_names', None)  # Remove tag_names from task data

        # Create the task with new fields
        db_task = Task(**task_data, owner_id=current_user_id)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        # Get the ID before the session is committed to use later
        task_id = db_task.id

        # Handle tags after task is created
        task_tags = []
        if tag_names:
            for tag_name in tag_names:
                # Find or create tag
                tag = session.exec(select(Tag).where(Tag.name == tag_name).where(Tag.user_id == current_user_id)).first()
                if not tag:
                    tag = Tag(name=tag_name, user_id=current_user_id)
                    session.add(tag)

                task_tags.append(tag.name)

        session.commit()

        # Create response using attribute-based validation to avoid SQLAlchemy object issues
        task_read = TaskRead.model_validate(db_task, from_attributes=True).model_copy(
            update={"tags": list(task_tags) if task_tags else []}
        )

        # Publish event to Dapr
        try:
            dapr_client.initialize()
            event_data = {
                "task_id": db_task.id,
                "user_id": current_user_id,
                "title": db_task.title,
                "description": db_task.description,
                "priority": db_task.priority,
                "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                "recurrence_pattern": db_task.recurrence_pattern,
                "tags": task_tags,
                "created_at": db_task.created_at.isoformat()
            }
            dapr_client.publish_task_event("task.created", event_data)
        except Exception as e:
            print(f"[ERROR] Failed to publish task.created event: {str(e)}")
            # Don't fail the whole operation if event publishing fails

        print(f"[TASK] Task created successfully: {db_task.id}")
        return task_read
    except Exception as e:
        session.rollback()  # Rollback on error
        print(f"[ERROR] Error creating task: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )

@app.get("/api/tasks", response_model=List[TaskRead])
def read_tasks(
    *,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
    priority: Optional[str] = None,
    status: Optional[str] = None,
    tag: Optional[str] = None,
    due_date_start: Optional[str] = None,
    due_date_end: Optional[str] = None,
    search: Optional[str] = None
):
    try:
        # Base query
        statement = select(Task).where(Task.owner_id == current_user_id)

        # Apply filters
        if priority:
            statement = statement.where(Task.priority == priority)
        if status:
            if status == "completed":
                statement = statement.where(Task.is_completed == True)
            elif status == "pending":
                statement = statement.where(Task.is_completed == False)
        if due_date_start:
            start_date = datetime.fromisoformat(due_date_start.replace('Z', '+00:00'))
            statement = statement.where(Task.due_date >= start_date)
        if due_date_end:
            end_date = datetime.fromisoformat(due_date_end.replace('Z', '+00:00'))
            statement = statement.where(Task.due_date <= end_date)
        if search:
            # Full-text search across title and description
            statement = statement.where(
                (Task.title.contains(search)) |
                (Task.description.contains(search))
            )

        tasks = session.exec(statement).all()

        # Add tags to each task
        result_tasks = []
        for task in tasks:
            # Find all tags linked to this specific task
            task_tag_links = session.exec(
                select(TaskTagLink).where(TaskTagLink.task_id == task.id)
            ).all()

            tag_ids = [link.tag_id for link in task_tag_links]
            task_tags = []
            if tag_ids:
                tag_records = session.exec(
                    select(Tag).where(Tag.id.in_(tag_ids))
                ).all()
                task_tags = [tag.name for tag in tag_records]

            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_completed": task.is_completed,
                "priority": task.priority,
                "due_date": task.due_date,
                "recurrence_pattern": task.recurrence_pattern,
                "owner_id": task.owner_id,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "tags": task_tags
            }
            result_tasks.append(TaskRead(**task_dict))

        return result_tasks
    except Exception as e:
        print(f"Error reading tasks: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading tasks: {str(e)}"
        )

@app.get("/api/tasks/{task_id}", response_model=TaskRead)
def read_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    current_user_id: str = Depends(get_current_user_id)
):
    try:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")
        return task
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        print(f"Error reading task: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading task: {str(e)}"
        )

@app.put("/api/tasks/{task_id}", response_model=TaskRead)
def update_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    task_in: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    try:
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        if db_task.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        # Extract tag names before updating the task
        tag_names = getattr(task_in, 'tag_names', [])

        # Prepare task data excluding tag_names
        task_data = task_in.model_dump(exclude_unset=True)
        task_data.pop('tag_names', None)  # Remove tag_names from task data

        # Store original values for event
        original_title = db_task.title
        original_description = db_task.description
        original_priority = db_task.priority
        original_due_date = db_task.due_date
        original_recurrence_pattern = db_task.recurrence_pattern
        original_is_completed = db_task.is_completed

        # Update task fields
        for key, value in task_data.items():
            setattr(db_task, key, value)

        # Handle tags
        if tag_names is not None:
            # Remove all existing tag links for this task
            existing_links = session.exec(
                select(TaskTagLink).where(TaskTagLink.task_id == task_id)
            ).all()
            for link in existing_links:
                session.delete(link)

            # Add new tags
            for tag_name in tag_names:
                # Find or create tag
                tag = session.exec(select(Tag).where(Tag.name == tag_name).where(Tag.user_id == current_user_id)).first()
                if not tag:
                    tag = Tag(name=tag_name, user_id=current_user_id)
                    session.add(tag)
                    session.flush()  # Get the tag ID

                # Create link between task and tag
                task_tag_link = TaskTagLink(task_id=db_task.id, tag_id=tag.id)
                session.add(task_tag_link)

        db_task.updated_at = datetime.now(timezone.utc)
        session.add(db_task)
        session.commit()

        # Refresh and return the task with tags
        task_tags = session.exec(
            select(Tag.name).join(TaskTagLink).where(TaskTagLink.task_id == db_task.id)
        ).all()
        task_dict = {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "is_completed": db_task.is_completed,
            "priority": db_task.priority,
            "due_date": db_task.due_date,
            "recurrence_pattern": db_task.recurrence_pattern,
            "owner_id": db_task.owner_id,
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at,
            "tags": list(task_tags)
        }

        # Publish event to Dapr
        try:
            dapr_client.initialize()
            event_data = {
                "task_id": db_task.id,
                "user_id": current_user_id,
                "original_title": original_title,
                "original_description": original_description,
                "original_priority": original_priority,
                "original_due_date": original_due_date.isoformat() if original_due_date else None,
                "original_recurrence_pattern": original_recurrence_pattern,
                "original_is_completed": original_is_completed,
                "updated_fields": task_data,
                "title": db_task.title,
                "description": db_task.description,
                "priority": db_task.priority,
                "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                "recurrence_pattern": db_task.recurrence_pattern,
                "is_completed": db_task.is_completed,
                "tags": task_tags,
                "updated_at": db_task.updated_at.isoformat()
            }
            dapr_client.publish_task_event("task.updated", event_data)
        except Exception as e:
            print(f"[ERROR] Failed to publish task.updated event: {str(e)}")
            # Don't fail the whole operation if event publishing fails

        return TaskRead(**task_dict)
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        session.rollback()  # Rollback on error
        print(f"Error updating task: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )

@app.delete("/api/tasks/{task_id}")
def delete_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    current_user_id: str = Depends(get_current_user_id)
):
    try:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        # Get task data before deletion for the event
        task_data = {
            "task_id": task.id,
            "user_id": current_user_id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "recurrence_pattern": task.recurrence_pattern,
            "is_completed": task.is_completed,
            "created_at": task.created_at.isoformat(),
            "deleted_at": datetime.now(timezone.utc).isoformat()
        }

        session.delete(task)
        session.commit()

        # Publish event to Dapr
        try:
            dapr_client.initialize()
            dapr_client.publish_task_event("task.deleted", task_data)
        except Exception as e:
            print(f"[ERROR] Failed to publish task.deleted event: {str(e)}")
            # Don't fail the whole operation if event publishing fails

        return {"status": "success"}
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        session.rollback()  # Rollback on error
        print(f"Error deleting task: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )

@app.patch("/api/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_complete(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    current_user_id: str = Depends(get_current_user_id)
):
    try:
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        if db_task.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        was_completed = db_task.is_completed
        db_task.is_completed = not db_task.is_completed
        db_task.updated_at = datetime.now(timezone.utc)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        # Publish event to Dapr
        try:
            dapr_client.initialize()
            event_data = {
                "task_id": db_task.id,
                "user_id": current_user_id,
                "was_completed": was_completed,
                "is_now_completed": db_task.is_completed,
                "title": db_task.title,
                "completed_at": db_task.updated_at.isoformat()
            }

            event_type = "task.completed" if db_task.is_completed else "task.uncompleted"
            dapr_client.publish_task_event(event_type, event_data)
        except Exception as e:
            print(f"[ERROR] Failed to publish task completion event: {str(e)}")
            # Don't fail the whole operation if event publishing fails

        return db_task
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        session.rollback()  # Rollback on error
        print(f"Error toggling task completion: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling task completion: {str(e)}"
        )

@app.get("/api/tags", response_model=List[str])
def read_tags(
    *,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get all tags for the current user"""
    try:
        tags = session.exec(select(Tag.name).where(Tag.user_id == current_user_id)).all()
        return tags
    except Exception as e:
        print(f"Error reading tags: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading tags: {str(e)}"
        )


@app.post("/api/tasks/{task_id}/tags", response_model=TaskRead)
def add_tags_to_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    tag_names: List[str],
    current_user_id: str = Depends(get_current_user_id)
):
    """Add tags to a specific task"""
    try:
        # Verify task belongs to user
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        if db_task.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        # Add tags to the task
        for tag_name in tag_names:
            # Find or create tag
            tag = session.exec(select(Tag).where(Tag.name == tag_name).where(Tag.user_id == current_user_id)).first()
            if not tag:
                tag = Tag(name=tag_name, user_id=current_user_id)
                session.add(tag)
                session.flush()  # Get the tag ID

            # Create link between task and tag if it doesn't exist
            existing_link = session.exec(
                select(TaskTagLink).where(TaskTagLink.task_id == task_id).where(TaskTagLink.tag_id == tag.id)
            ).first()

            if not existing_link:
                task_tag_link = TaskTagLink(task_id=task_id, tag_id=tag.id)
                session.add(task_tag_link)

        session.commit()

        # Return updated task with tags
        task_tags = session.exec(
            select(Tag.name).join(TaskTagLink).where(TaskTagLink.task_id == db_task.id)
        ).all()
        task_dict = {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "is_completed": db_task.is_completed,
            "priority": db_task.priority,
            "due_date": db_task.due_date,
            "recurrence_pattern": db_task.recurrence_pattern,
            "owner_id": db_task.owner_id,
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at,
            "tags": list(task_tags)
        }

        return TaskRead(**task_dict)
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        session.rollback()  # Rollback on error
        print(f"Error adding tags to task: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding tags to task: {str(e)}"
        )


@app.delete("/api/tasks/{task_id}/tags", response_model=TaskRead)
def remove_tags_from_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    tag_names: List[str],
    current_user_id: str = Depends(get_current_user_id)
):
    """Remove specific tags from a task"""
    try:
        # Verify task belongs to user
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        if db_task.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        # Remove specific tags from the task
        for tag_name in tag_names:
            tag = session.exec(select(Tag).where(Tag.name == tag_name).where(Tag.user_id == current_user_id)).first()
            if tag:
                # Delete the link between task and tag
                link_to_delete = session.exec(
                    select(TaskTagLink).where(TaskTagLink.task_id == task_id).where(TaskTagLink.tag_id == tag.id)
                ).first()

                if link_to_delete:
                    session.delete(link_to_delete)

        session.commit()

        # Return updated task with remaining tags
        task_tags = session.exec(
            select(Tag.name).join(TaskTagLink).where(TaskTagLink.task_id == db_task.id)
        ).all()
        task_dict = {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "is_completed": db_task.is_completed,
            "priority": db_task.priority,
            "due_date": db_task.due_date,
            "recurrence_pattern": db_task.recurrence_pattern,
            "owner_id": db_task.owner_id,
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at,
            "tags": list(task_tags)
        }

        return TaskRead(**task_dict)
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        session.rollback()  # Rollback on error
        print(f"Error removing tags from task: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing tags from task: {str(e)}"
        )


@app.get("/api/tasks/{task_id}", response_model=TaskRead)
def read_task(
    *,
    session: Session = Depends(get_session),
    task_id: int,
    current_user_id: str = Depends(get_current_user_id)
):
    try:
        # Load task
        db_task = session.get(Task, task_id)

        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        if db_task.owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this resource")

        # Get tags for this task
        task_tags = session.exec(
            select(Tag.name)
            .join(TaskTagLink).where(TaskTagLink.task_id == task_id)
        ).all()

        task_dict = {
            "id": db_task.id,
            "title": db_task.title,
            "description": db_task.description,
            "is_completed": db_task.is_completed,
            "priority": db_task.priority,
            "due_date": db_task.due_date,
            "recurrence_pattern": db_task.recurrence_pattern,
            "owner_id": db_task.owner_id,
            "created_at": db_task.created_at,
            "updated_at": db_task.updated_at,
            "tags": list(task_tags)
        }
        return TaskRead(**task_dict)
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        print(f"Error reading task: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading task: {str(e)}"
        )


@app.get("/api/debug/cors")
async def debug_cors():
    """Debug endpoint to check CORS configuration"""
    return {
        "cors_origins": cors_origins,
        "message": "CORS is working correctly if you received this response"
    }


# New endpoints for advanced features

@app.get("/api/tasks/recurring")
def get_recurring_tasks(
    *,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get all recurring tasks for the user"""
    try:
        recurring_tasks = session.exec(
            select(Task).where(
                Task.owner_id == current_user_id
            ).where(
                Task.recurrence_pattern.is_not(None)
            )
        ).all()
        return recurring_tasks
    except Exception as e:
        print(f"Error getting recurring tasks: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting recurring tasks: {str(e)}"
        )


@app.get("/api/tasks/due-soon")
def get_due_soon_tasks(
    *,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id),
    days_ahead: int = 7  # Default to 7 days ahead
):
    """Get tasks that are due soon"""
    try:
        from datetime import timedelta
        now = datetime.now(timezone.utc)
        future_date = now + timedelta(days=days_ahead)

        due_soon_tasks = session.exec(
            select(Task).where(
                Task.owner_id == current_user_id
            ).where(
                Task.due_date.is_not(None)
            ).where(
                Task.due_date <= future_date
            ).where(
                Task.is_completed == False
            )
        ).all()
        return due_soon_tasks
    except Exception as e:
        print(f"Error getting due soon tasks: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting due soon tasks: {str(e)}"
        )


@app.get("/api/tasks/stats")
def get_task_stats(
    *,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get task statistics for the user"""
    try:
        total_tasks = session.exec(
            select(Task).where(Task.owner_id == current_user_id)
        ).all()

        completed_tasks = session.exec(
            select(Task).where(
                Task.owner_id == current_user_id
            ).where(Task.is_completed == True)
        ).all()

        pending_tasks = session.exec(
            select(Task).where(
                Task.owner_id == current_user_id
            ).where(Task.is_completed == False)
        ).all()

        # Count by priority
        high_priority_count = len(session.exec(
            select(Task).where(
                Task.owner_id == current_user_id
            ).where(Task.priority == "high")
        ).all())

        medium_priority_count = len(session.exec(
            select(Task).where(
                Task.owner_id == current_user_id
            ).where(Task.priority == "medium")
        ).all())

        low_priority_count = len(session.exec(
            select(Task).where(
                Task.owner_id == current_user_id
            ).where(Task.priority == "low")
        ).all())

        return {
            "total": len(total_tasks),
            "completed": len(completed_tasks),
            "pending": len(pending_tasks),
            "high_priority": high_priority_count,
            "medium_priority": medium_priority_count,
            "low_priority": low_priority_count
        }
    except Exception as e:
        print(f"Error getting task stats: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting task stats: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
