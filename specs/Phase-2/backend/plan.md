# Implementation Plan: Phase 2 Backend

## Phase 1: Environment & Scaffolding
- [ ] Initialize Python 3.13 project with `pyproject.toml` or `requirements.txt`.
- [ ] Install dependencies: `fastapi`, `uvicorn`, `sqlmodel`, `psycopg2-binary`, `python-jose[cryptography]`, `pydantic-settings`.
- [ ] Configure `.env` with `DATABASE_URL` (Neon) and `BETTER_AUTH_SECRET`.
- [ ] Setup FastAPI base application and logging.

## Phase 2: Data Layer (SQLModel & Neon)
- [ ] Define `User` and `Task` models in `models.py`.
- [ ] Create database engine with connection pooling settings.
- [ ] Implement a `get_session` dependency for FastAPI.
- [ ] Run initial migrations or `SQLModel.metadata.create_all(engine)` (for dev).

## Phase 3: Security & Middleware
- [ ] Create `auth.py` to handle JWT decoding.
- [ ] Implement `get_current_user` dependency that:
  - Extracts token from header.
  - Decodes token using `BETTER_AUTH_SECRET`.
  - Validates user existence (optional, depending on auth strategy).
- [ ] Setup CORS middleware to allow requests from the Next.js frontend.

## Phase 4: API Endpoints
- [ ] **POST /api/tasks:** Implement creation logic with `user_id` injection.
- [ ] **GET /api/tasks:** Implement listing with filter `owner_id == current_user.id`.
- [ ] **GET /api/tasks/{id}:** Implement detail retrieval with ownership check.
- [ ] **PUT /api/tasks/{id}:** Implement update logic with ownership check.
- [ ] **DELETE /api/tasks/{id}:** Implement deletion logic with ownership check.
- [ ] **PATCH /api/tasks/{id}/complete:** Implement specialized toggle logic.

## Phase 5: Testing & Deployment
- [ ] Write unit tests for business logic (ownership validation).
- [ ] Write integration tests using `TestClient` and an override for `get_current_user`.
- [ ] Configure `vercel.json` or Railway `Dockerfile`.
- [ ] Deploy and verify with Neon production database.

## Critical Edge Cases to Test
- **Unauthorized Access:** Ensure `User A` cannot see/edit/delete `User B`'s tasks.
- **Malformed Tokens:** Ensure API returns `401` for expired or tampered JWTs.
- **Large Payloads:** Validate `title` and `description` length limits.
- **Database Connection Failures:** Implement graceful error handling if Neon is unreachable.
