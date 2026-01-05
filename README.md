# Todo Evolution: Spec-Driven Development Hackathon

## Project Overview
This project is a 5-phase evolution of a Todo application, starting from a simple Python console app and scaling into a distributed, cloud-native, AI-integrated system. We use a **Spec-Driven Development** approach, where every feature is meticulously defined before implementation.

## The 5 Phases
1.  **Phase 1: In-Memory Python Console App** (✅ Complete)
    -   Basic CRUD with priorities and tags in a CLI environment.
2.  **Phase 2: Full-Stack Web Application** (🎯 Next)
    -   Next.js 15, FastAPI, Neon PostgreSQL, and Better Auth.
3.  **Phase 3: AI-Powered Todo Chatbot**
    -   Conversational interface using OpenAI Agents SDK and MCP.
4.  **Phase 4: Local Kubernetes Deployment**
    -   Containerization and orchestration on Minikube.
5.  **Phase 5: Advanced Cloud Deployment**
    -   Distributed system on DOKS with Kafka and Dapr.

## Repository Structure
-   `.claude/agents/`: Reusable specialized agents shared across all phases.
-   `.specify/memory/constitution.md`: Global rules and phase definitions (The "Source of Truth").
-   `specs/`: Detailed functional and technical specifications organized by phase.
-   `Phase-X/`: Independent, self-contained implementation directories for each phase.

## Tech Stack (Global)
-   **Backend:** Python (FastAPI), SQLModel.
-   **Frontend:** TypeScript (Next.js 15).
-   **Database:** Neon (PostgreSQL).
-   **Infrastructure:** Docker, Kubernetes, Kafka, Dapr.
-   **AI:** OpenAI Agents SDK, Claude Code.

## Getting Started
Each phase directory contains its own `README.md` with specific setup and run instructions.
-   See [Phase-1/README.md](./Phase-1/README.md) for the CLI app.

---
🤖 *Spec-driven, AI-accelerated evolution.*
