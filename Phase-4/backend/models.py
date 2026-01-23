from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
import sqlmodel
from typing import Optional, List
from datetime import datetime, timezone
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column("createdAt"))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column("updatedAt"))
    tasks: List["Task"] = Relationship(back_populates="owner")

class TaskBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    owner: User = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskRead(TaskBase):
    id: int
    owner_id: str
    created_at: datetime
    updated_at: datetime
