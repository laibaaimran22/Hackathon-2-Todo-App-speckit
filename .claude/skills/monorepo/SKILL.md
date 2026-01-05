# Monorepo Management Skill

## Overview
This skill focuses on organizing and managing multi-service projects within a single repository. It emphasizes a clean separation of concerns, efficient local development workflows, and streamlined deployment paths for full-stack applications (e.g., Next.js + FastAPI).

## Core Capabilities
- **Structural Integrity**: Organizing services into dedicated subdirectories (e.g., `frontend/`, `backend/`) while maintaining root-level shared configuration.
- **Concurrent Development**: Workflows for running multiple services simultaneously using tools like Docker Compose or `concurrently`.
- **Environment Management**: Handling shared secrets and service-specific `.env` files across the monorepo.
- **Deployment Strategy**: Implementing multi-platform deployment pipelines (e.g., Vercel for Frontend, Railway/DOKS for Backend).

## Recommended Structure
```text
Phase-X/
├── frontend/           # Next.js Application
│   ├── src/
│   ├── .env.local
│   └── package.json
├── backend/            # FastAPI Application
│   ├── app/
│   ├── .env
│   └── main.py
├── docker-compose.yml  # Local orchestration
└── README.md           # Phase orchestration guide
```

## Local Development (Docker Compose)
Example `docker-compose.yml` for local orchestration:
```yaml
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    env_file: ./frontend/.env.local
  backend:
    build: ./backend
    ports: ["8000:8000"]
    env_file: ./backend/.env
```

## Best Practices
1.  **Isolation**: Ensure services do not import code directly from each other. Communication should happen via HTTP/REST.
2.  **Shared Config**: Keep global configuration (like the project Constitution or shared GitHub Actions) at the repository root.
3.  **Cross-Origin (CORS)**: Always configure the backend to explicitly allow the frontend's origin during development and production.
4.  **Uniform Tooling**: Use consistent linting and formatting rules across all directories where possible.
5.  **Clean Roots**: Avoid cluttering the monorepo root with service-specific files.

## Deployment Paths
- **Frontend**: Vercel (Native Next.js support).
- **Backend**: Railway, Hugging Face, or Render for persistent FastAPI services.
- **Database**: Neon (Serverless PostgreSQL) shared by both services.

## Example Usage
> "Set up a monorepo structure for Phase 2 with Next.js and FastAPI, including a Docker Compose file for local development and a deployment plan for Vercel and Railway."
