# Tasks: Phase 2 Backend Implementation

This task list defines the development path for the Phase 2 FastAPI Backend, ensuring alignment with the SDD process and multi-tenant security requirements.

## Phase 1: Environment & Scaffolding
- [x] **Task 1: Project Initialization**
  - Create `Phase-2/backend/pyproject.toml` or `requirements.txt`.
  - Include dependencies: `fastapi`, `uvicorn`, `sqlmodel`, `psycopg2-binary`, `python-jose[cryptography]`, `pydantic-settings`, `python-dotenv`.
  - **Done Criteria**: Dependencies install without conflict. (✅ COMPLETED)
- [x] **Task 2: Environment Configuration**
  - Create `.env` in `Phase-2/backend/`.
  - Define `DATABASE_URL`, `BETTER_AUTH_SECRET`, and `CORS_ORIGINS`.
  - **Done Criteria**: `.env` is populated and excluded from Git via `.gitignore`. (✅ COMPLETED)
- [x] **Task 3: FastAPI Entry Point**
  - Create `Phase-2/backend/main.py`.
  - Initialize `app = FastAPI()`.
  - Add basic health check endpoint at `GET /health`.
  - **Done Criteria**: `uvicorn main:app` starts the server on port 8000. (✅ COMPLETED)

## Phase 2: Data Persistence (SQLModel)
- [x] **Task 4: Database Connection Infrastructure**
  - Create `Phase-2/backend/database.py`.
  - Setup the SQLModel engine with SSL mode for Neon.
  - Implement `init_db()` and `get_session()` generator.
  - **Done Criteria**: Successful connection to the Neon database instance. (✅ COMPLETED)
- [x] **Task 5: Schema Definition**
  - Create `Phase-2/backend/models.py`.
  - Define `User` table (id, email).
  - Define `Task` table (id, title, description, is_completed, created_at, owner_id).
  - Add foreign key from `Task.owner_id` to `User.id`.
  - **Done Criteria**: Models reflect the `data-model.md` specification. (✅ COMPLETED)

## Phase 3: Security & Middleware
- [x] **Task 6: Authentication Logic**
  - Create `Phase-2/backend/auth.py`.
  - Implement `verify_token(token: str)` using `BETTER_AUTH_SECRET`.
  - Implement `get_current_user` dependency to extract `sub` from JWT.
  - **Done Criteria**: Middleware correctly decodes and validates valid JWTs. (✅ COMPLETED)
- [x] **Task 7: CORS Configuration**
  - Add `CORSMiddleware` to `main.py`.
  - Allow `http://localhost:3000`.
  - **Done Criteria**: Pre-flight OPTIONS requests from frontend succeed. (✅ COMPLETED)

## Phase 4: REST API Endpoints (CRUD)
- [x] **Task 8: Create Task (POST /tasks)**
  - Implement endpoint with `TaskCreate` Pydantic schema.
  - Inject `current_user` and assign to `owner_id`.
  - **Done Criteria**: New task is saved with the correct owner ID. (✅ COMPLETED)
- [x] **Task 9: List Tasks (GET /tasks)**
  - Implement endpoint returning `List[Task]`.
  - Filter by `owner_id == current_user.id`.
  - **Done Criteria**: User receives ONLY their own tasks. (✅ COMPLETED)
- [x] **Task 10: Task Management (GET, PUT, DELETE /{id})**
  - Implement individual CRUD endpoints with ownership verification.
  - Raise `403 Forbidden` if user tries to access tasks owned by others.
  - **Done Criteria**: Full CRUD lifecycle working with strict isolation. (✅ COMPLETED)
- [x] **Task 11: Specialized Completion Logic (PATCH /{id}/complete)**
  - Implement toggle logic or explicit status update.
  - **Done Criteria**: Task status updates correctly. (✅ COMPLETED)

## Phase 5: Verification & Cleanup
- [x] **Task 12: Documentation Verification**
  - Access `/docs` (Swagger) and verify all endpoints match the `api-contract.md`.
  - **Done Criteria**: No schema mismatches between spec and implementation. (✅ COMPLETED)
- [x] **Task 13: End-to-End Manual Testing**
  - Use a test JWT to verify the full flow (Create -> List -> Update -> Delete).
  - **Done Criteria**: All 6 REST operations pass manual verification. (✅ COMPLETED)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
