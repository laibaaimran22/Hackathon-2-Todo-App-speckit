from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from pydantic import BaseModel
from jose import jwt
import secrets

from database import engine, get_session, init_db
from models import Task, TaskCreate, TaskRead, TaskUpdate, User
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

# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# CORS Configuration - Split comma-separated string into list
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Now a proper list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    secret = os.getenv("JWT_SECRET") or os.getenv("BETTER_AUTH_SECRET")
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
    secret = os.getenv("JWT_SECRET") or os.getenv("BETTER_AUTH_SECRET")
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
async def get_user(current_user_id: str = Depends(get_current_user_id)):
    # Return user info based on the authenticated user
    return {
        "id": current_user_id,
        "email": f"{current_user_id}@example.com"
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
        # Ensure user exists in our DB (Lazy upsert)
        user = session.get(User, current_user_id)
        if not user:
            # We don't have the email from JWT here easily without more decoding,
            # but Better Auth provides it. For now, we use a placeholder or decode more.
            user = User(id=current_user_id, email=f"{current_user_id}@placeholder.com")
            session.add(user)
            session.flush()  # Use flush instead of commit to keep in same transaction

        task_data = task_in.model_dump()
        db_task = Task(**task_data, owner_id=current_user_id)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except Exception as e:
        session.rollback()  # Rollback on error
        print(f"Error creating task: {str(e)}")
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
    current_user_id: str = Depends(get_current_user_id)
):
    try:
        tasks = session.exec(select(Task).where(Task.owner_id == current_user_id)).all()
        return tasks
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

        task_data = task_in.model_dump(exclude_unset=True)
        for key, value in task_data.items():
            setattr(db_task, key, value)

        db_task.updated_at = datetime.now(timezone.utc)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
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

        session.delete(task)
        session.commit()
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

        db_task.is_completed = not db_task.is_completed
        db_task.updated_at = datetime.now(timezone.utc)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
