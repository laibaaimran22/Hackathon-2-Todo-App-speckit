from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime
import sqlmodel
from typing import Optional, List
from datetime import datetime, timezone
from pydantic import ConfigDict

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)

class TaskBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    is_completed: bool = Field(default=False)
    priority: Optional[str] = Field(default="medium", max_length=10)  # high/medium/low
    due_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    recurrence_pattern: Optional[str] = Field(default=None, max_length=50)  # daily/weekly/monthly

class User(UserBase, table=True):
    id: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column("createdAt"))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column("updatedAt"))
    tasks: List["Task"] = Relationship(back_populates="owner")
    tags: List["Tag"] = Relationship(back_populates="user")

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    user_id: str = Field(foreign_key="user.id", index=True)  # Tags belong to a user

    # Relationships
    user: User = Relationship(back_populates="tags")

class TaskTagLink(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    owner: User = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    # Allow tags to be passed during creation
    tag_names: Optional[List[str]] = []

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    tag_names: Optional[List[str]] = []

class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: str
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []  # Return tag names as strings for simplicity
