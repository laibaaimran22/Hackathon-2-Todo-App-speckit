# FastAPI Backend Development Skill

## Overview
This skill focuses on building high-performance, production-ready REST APIs using **FastAPI**, **SQLModel**, and **Pydantic**. It emphasizes clean architecture, type safety, and efficient database management for modern web applications.

## Core Capabilities
- **RESTful API Design**: Structure endpoints logically by feature (e.g., `/tasks`, `/users`) using `APIRouter`.
- **Validation (Pydantic)**: Enforce strict data validation and serialization for request bodies and response models.
- **Persistence (SQLModel)**: Seamlessly integrate Python classes with SQL databases (PostgreSQL/Neon) using SQLModel ORM.
- **Dependency Injection**: Manage database sessions, authentication, and configuration through FastAPI's robust DI system.
- **Security (JWT)**: Implement secure authentication and authorization patterns using JWT tokens and OAuth2 password flows.
- **Async Programming**: Utilize `async`/`await` for non-blocking I/O operations (database queries, external API calls).

## Best Practices
1.  **Feature-Based Organization**: Group routers, models, and services by feature rather than layer (e.g., `src/features/tasks/...`).
2.  **Schema Separation**: Use separate models for **Table** (SQLModel), **Create** (Pydantic), and **Read** (Pydantic) to avoid exposing internal IDs or passwords.
3.  **Endpoint Typing**: Always use `response_model` and type hints for path/query parameters.
4.  **Error Handling**: Centralize error responses using `HTTPException` and custom exception handlers.
5.  **Environment Stability**: Manage secrets and configuration via `.env` files using `pydantic-settings`.

## Integration Highlights (Phase 2+)
- **Neon DB**: Optimized for serverless PostgreSQL connections.
- **Better Auth Integration**: Coordinating with Next.js frontend for secure session management.
- **CORS Configuration**: Proper setup for multi-service communication between frontend and backend.

## Example Usage
> "Architect a task-management API with a PostgreSQL backend using SQLModel, including paginated list endpoints and optimistic locking."
