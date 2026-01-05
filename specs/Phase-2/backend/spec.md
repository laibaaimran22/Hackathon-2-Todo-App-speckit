# Specification: Phase 2 Backend - Authenticated REST API

## Project Overview
The goal of Phase 2 Backend is to transition from an in-memory console application to a persistent, authenticated REST API. This API will serve as the foundation for the Todo Management system, enabling multi-user support with strict data isolation.

**Tech Stack:**
- **Language:** Python 3.13+
- **Framework:** FastAPI
- **ORM:** SQLModel (built on SQLAlchemy and Pydantic)
- **Database:** Neon PostgreSQL (Serverless)
- **Authentication:** JWT-based (python-jose) using `BETTER_AUTH_SECRET`
- **Deployment:** Vercel or Railway

## User Stories

### Authentication & Identification (Internal)
- **Story:** As a System Developer, I want to verify JWT tokens in incoming requests, so that I can identify the authenticated user and secure resources.
- **AC 1:** Middleware or dependency must extract the Bearer token from the `Authorization` header.
- **AC 2:** Tokens must be decoded using the `BETTER_AUTH_SECRET` environment variable.
- **AC 3:** Invalid or expired tokens must return a `401 Unauthorized` response with a clear error message.

### Todo Management
- **Story:** As an Authenticated User, I want to create, read, update, and delete my tasks, so that I can manage my productivity without seeing others' data.
- **AC 1:** All task-related endpoints must filter or validate actions based on the `user_id` extracted from the JWT.
- **AC 2:** Attempting to access or modify a task belonging to another user must return a `404 Not Found` (to avoid data leaking) or `403 Forbidden`.
- **AC 3:** The list endpoint (`GET /api/tasks`) must only return tasks created by the current user.

## Functional Requirements

### Task CRUD Operations
1. **Create Task:** Accepts title, description, and status. Automatically assigns `owner_id` from JWT.
2. **List Tasks:** Returns a list of tasks owned by the user.
3. **Get Task Details:** Returns full details of a specific task if owned by the user.
4. **Update Task:** Allows modification of fields. Validates ownership before saving.
5. **Delete Task:** Removes task from database. Validates ownership.
6. **Toggle Completion:** Specialized PATCH endpoint to quickly mark a record as complete/incomplete.

## Non-Functional Requirements

### Performance
- **Latency:** API responses (excluding cold starts) must be under 200ms for standard CRUD operations.
- **Concurrency:** Support for concurrent database connections handled by Neon's connection pooling.

### Security
- **Data Isolation:** Row-level isolation enforced at the application level via `WHERE user_id = current_user_id`.
- **Secrets Management:** Sensitive variables like `DATABASE_URL` and `BETTER_AUTH_SECRET` must never be hardcoded.
- **Input Validation:** Use Pydantic models to strictly validate incoming payloads to prevent injection or malformed data.

### Reliability
- **Error States:**
  - `400 Bad Request` for validation failures.
  - `401 Unauthorized` for missing/invalid auth.
  - `403 Forbidden` for unauthorized resource access.
  - `404 Not Found` for non-existent or inaccessible IDs.
  - `500 Internal Server Error` for unhandled exceptions (logged for debugging).

## Constraints & Assumptions
- **User Source:** Users are managed externally (e.g., via a separate frontend auth service or shared database table). This API assumes the JWT contains a valid `sub` or `user_id`.
- **Hosting:** Optimized for Vercel (using serverless functions) or Railway (using containerized deployment).
- **Environment:** Requires `DATABASE_URL` (Neon) and `BETTER_AUTH_SECRET` to be configured.
