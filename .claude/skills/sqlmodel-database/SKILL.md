# SQLModel & Database Design Skill

## Overview
This skill focuses on designing and implementing robust data layers using **SQLModel** (a hybrid of SQLAlchemy and Pydantic) and **PostgreSQL (Neon)**. It emphasizes type safety, relationship management, and performance for modern serverless architectures.

## Core Capabilities
- **Model Definition**: Creating SQLModel classes that function as both database tables and data validation schemas.
- **Relationship Mapping**: Implementing one-to-many and many-to-many relationships using `Relationship` and `ForeignKey`.
- **Session Management**: Efficient handling of database sessions using FastAPI dependencies and engine pooling.
- **Neon Optimization**: Best practices for working with Neon's serverless PostgreSQL, including pooled connections and cold-start considerations.
- **Migrations & Constraints**: Defining indexes, unique constraints, and schema evolutions.

## Example Models

### User Table
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    hashed_password: str

    tasks: List["Task"] = Relationship(back_populates="owner")
```

### Task Table
```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    is_completed: bool = Field(default=False)

    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="tasks")
```

## Best Practices
1.  **Naming Conventions**: Use snake_case for fields and PascalCase for Models.
2.  **Indexing**: Apply `index=True` to fields frequently used in `WHERE` clauses (e.g., `username`, `email`).
3.  **Schema Separation**: Use separate models for **Table** (metadata), **Create** (input), and **Read** (output) to prevent data leaking.
4.  **Async/Await**: Always use `AsyncSession` for non-blocking database interactions in FastAPI.
5.  **Environment Integration**: Store the `DATABASE_URL` in an environment variable (e.g., `.env`).

## Example Usage
> "Design a relational schema for a multi-user Todo app with SQLModel, including User and Task tables with a one-to-many relationship and appropriate indexing."
