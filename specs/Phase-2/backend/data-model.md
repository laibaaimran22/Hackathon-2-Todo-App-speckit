# Data Model: Phase 2 Backend

## Entity Relationship Summary
The system utilizes a relational schema in Neon PostgreSQL. The primary relationship is between **Users** and **Tasks**, where a User can have many Tasks (**1:N**).

## Entities

### 1. User (SQLModel)
Represents an authenticated entity in the system.
- `id`: `UUID` or `String` (Primary Key) - Matches the `sub` claim in JWT.
- `email`: `String` (Unique)
- `created_at`: `DateTime`

### 2. Task (SQLModel)
Represents a todo item.
- `id`: `Integer` or `UUID` (Primary Key, Auto-increment/Generated)
- `title`: `String` (Required, Max 255 chars)
- `description`: `Text` (Optional)
- `is_completed`: `Boolean` (Default: `False`)
- `owner_id`: `String` (Foreign Key -> User.id, Indexed)
- `created_at`: `DateTime` (Default: `now()`)
- `updated_at`: `DateTime` (Automatic on update)

## Schema Definition (Logical)

```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    owner_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_owner_id ON tasks(owner_id);
```

## Implementation Notes (SQLModel/FastAPI)
- **Validation:** Use `Field(index=True)` for `owner_id`.
- **Automatic Timestamps:** Use SQLAlchemy `server_default` or FastAPI lifecycle events to handle `created_at` and `updated_at`.
- **Isolation:** Every query for tasks MUST include `.where(Task.owner_id == current_user.id)`.
