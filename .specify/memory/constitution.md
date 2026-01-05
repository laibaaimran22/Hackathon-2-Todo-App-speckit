# Todo Evolution - Spec-Driven Development Hackathon Constitution

## 1. PROJECT OVERVIEW
- **Project Name:** Todo Evolution - Spec-Driven Development Hackathon
- **Goal:** Build a progressively complex Todo application across 5 evolving phases, from a simple console app to a distributed cloud-native AI system.
- **Approach:** Spec-driven development using Claude Code and SpecKit Plus.
- **Repository Structure:** Single monorepo containing all phases in a centralized structure.

## 2. FIVE PHASES DEFINITION

### Phase 1: In-Memory Python Console App (✅ COMPLETE)
- **Technology:** Python 3.13+, UV
- **Features:** 5 basic CRUD operations (Add, Delete, Update, View, Mark Complete).
- **Storage:** In-memory (no database).
- **Deliverable:** Command-line todo manager.

### Phase 2: Full-Stack Web Application (🎯 CURRENT)
- **Technology:** Next.js 15 (App Router), FastAPI, SQLModel, Neon PostgreSQL, Better Auth.
- **Features:** Same 5 basic operations as web app with multi-user support.
- **Architecture:** Monorepo with `frontend/` and `backend/` inside `Phase-2/`.
- **Deliverable:** Full-stack web application with authentication and persistent storage.

### Phase 3: AI-Powered Todo Chatbot
- **Technology:** Phase 2 stack + OpenAI Agents SDK + Official MCP SDK.
- **Features:** All Phase 2 features + Natural language conversational interface.
- **Deliverable:** AI-powered conversational todo assistant.

### Phase 4: Local Kubernetes Deployment
- **Technology:** Phase 3 app + Docker, Minikube, Helm Charts, kubectl-ai, kagent.
- **Features:** All Phase 3 features deployed on local Kubernetes.
- **Deliverable:** Containerized orchestration on local Kubernetes.

### Phase 5: Advanced Cloud Deployment
- **Technology:** Phase 4 stack + Kafka, Dapr, DigitalOcean DOKS.
- **Features:** All Phase 4 features + Advanced features (Recurring tasks, Due dates, Priorities, Tags, Search, Filter, Sort).
- **Deliverable:** Production-grade distributed system on cloud with event-driven architecture.

## 3. GLOBAL DEVELOPMENT RULES

### Spec-Driven Development
- Every feature requires a specification BEFORE implementation.
- Specifications must include: user stories, acceptance criteria, edge cases, and constraints.
- No code should be written without an approved specification.
- Use SpecKit Plus workflows for specification management.

### Phase Implementation Order
- Phases MUST be completed sequentially (1 → 2 → 3 → 4 → 5).
- No skipping phases or working on multiple phases simultaneously.
- A phase is considered complete only after full implementation and testing.

### Repository Structure Rules
- `specs/` folder at root level, organized by phase (e.g., `specs/Phase-1/`).
- `history/` folder at root level for prompt history records.
- `.claude/agents/` at root level, shared across ALL phases.
- Each phase has a dedicated directory: `Phase-1/`, `Phase-2/`, etc.
- Each phase directory must be self-contained.
- Root directory remains clean, containing only configuration and phase folders.

### Agent Usage
- Reusable agents in `.claude/agents/` are available for all phases.
- **Core Agents:** full-stack-spec-writer, system-architecture-designer, frontend-architect-nextjs, api-backend-architect, db-schema-architect, auth-security-architect, api-contract-architect, state-management-architect, system-integration-architect, todo-quality-architect, fault-tolerance-architect, performance-optimization-architect.

## 4. CODE QUALITY STANDARDS (All Phases)

### Type Safety
- **Frontend:** TypeScript (strict mode).
- **Backend:** Pydantic models for validation; SQLModel for ORM.

### Error Handling
- Comprehensive try-catch blocks for async operations.
- Proper HTTP status codes and user-friendly error messages.
- Graceful degradation and resilience.

### Security
- JWT-based authentication (from Phase 2 onwards).
- Input validation and sanitization.
- SQL injection and XSS prevention.
- Environment-based secret management (never committed to Git).

### Testing
- Unit tests for business logic.
- Integration tests for API endpoints.
- E2E tests for critical user flows.
- Target: Minimum 70% code coverage.

### Documentation
- `README.md` in each phase directory.
- OpenAPI/Swagger documentation for FastAPI backends.
- Clear setup and deployment instructions.

## 5. TECHNOLOGY STACK BY PHASE
- **Phase 1:** Python 3.13+, UV
- **Phase 2:** Next.js 15, FastAPI, SQLModel, Neon PostgreSQL, Better Auth, Tailwind CSS
- **Phase 3:** Phase 2 stack + OpenAI Agents SDK, Official MCP SDK
- **Phase 4:** Phase 3 stack + Docker, Kubernetes (Minikube), Helm, kubectl-ai, kagent
- **Phase 5:** Phase 4 stack + Apache Kafka, Dapr, DigitalOcean DOKS, GitHub Actions

## 6. DEPLOYMENT REQUIREMENTS
- **Phase 1:** Local execution.
- **Phase 2/3:** Frontend (Vercel), Backend (Vercel/Railway), Database (Neon).
- **Phase 4:** Local Kubernetes (Minikube).
- **Phase 5:** Production Kubernetes (DigitalOcean DOKS), Kafka (Redpanda Cloud).
