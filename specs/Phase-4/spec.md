# Phase 4: Local Kubernetes Deployment with Docker and Helm

## Overview
Phase 4 takes the completed Phase 3 application (Next.js frontend + FastAPI backend + Cohere AI chatbot currently deployed on Vercel + Hugging Face) and deploys it to a local Kubernetes cluster for development and testing.

## Target Audience
DevOps engineers deploying containerized Phase 3 todo application to local Kubernetes cluster using Minikube.

## Context
Phase 4 takes the completed Phase 3 application (Next.js frontend + FastAPI backend + Cohere AI chatbot currently deployed on Vercel + Hugging Face) and deploys it to a local Kubernetes cluster for development and testing.

## Focus
- Dockerize frontend and backend applications
- Create Kubernetes manifests for all resources
- Package application using Helm charts
- Deploy to Minikube (local Kubernetes)
- Maintain all Phase 3 features (authentication, CRUD, chatbot)
- Implement container security and best practices

## Success Criteria
- Frontend running in Kubernetes pods accessible via localhost
- Backend running in Kubernetes pods with internal networking
- All Phase 3 features working (login, signup, add/edit/delete tasks, chatbot)
- Docker images optimized (<500MB frontend, <300MB backend)
- Helm chart successfully deploys entire stack
- Application scales horizontally with kubectl scale
- Health checks and readiness probes functional
- Rolling updates work without downtime
- All secrets managed securely via Kubernetes Secrets
- Resource limits and requests properly configured

## Constraints
- Working Directory: Phase-4/ (copy of Phase-3 with additions)
- Specifications: specs/Phase-4/
- History: history/Phase-4/
- Deployment Target: Local Kubernetes (Minikube) ONLY
- Technology: Docker, Kubernetes, Helm, Minikube, kubectl
- Database: External Neon PostgreSQL (not containerized)
- No cloud deployment (purely local)
- Must maintain ALL Phase 3 functionality

## Architecture
```
User (localhost browser)
↓
Minikube Ingress/Service
↓
Frontend Pods (Next.js in containers)
↓
Backend Service (Kubernetes service)
↓
Backend Pods (FastAPI in containers)
↓
External Neon PostgreSQL Database
```

## Key Components

### 1. Docker Containerization:
- Multi-stage Dockerfiles for frontend and backend
- Optimized image sizes
- Non-root user execution
- Health check endpoints
- .dockerignore files

### 2. Kubernetes Manifests:
- Deployments (2 replicas each for frontend/backend)
- Services (LoadBalancer/NodePort for frontend, ClusterIP for backend)
- ConfigMaps (non-sensitive configuration)
- Secrets (API keys, database URLs, JWT secrets)
- Optional Ingress for routing

### 3. Helm Chart:
- Chart.yaml with metadata
- values.yaml for configuration
- Templates for all Kubernetes resources
- Parameterized for different environments

### 4. Deployment Process:
- Build Docker images locally
- Load images into Minikube
- Create Kubernetes secrets
- Deploy using Helm or kubectl
- Verify all pods running
- Access application via Minikube service URL

## Functional Requirements:

### FR-001: Frontend Dockerization
- Create Dockerfile with multi-stage build
- Base image: node:18-alpine or node:20-alpine
- Build stage: install deps, build Next.js app
- Runtime stage: serve built app with standalone output
- Expose port 3000
- Health check on /api/health
- Image size target: <500MB

### FR-002: Backend Dockerization
- Create Dockerfile with Python slim base
- Install production dependencies only
- Copy application code
- Non-root user execution
- Expose port 8000
- Health check on /health
- Image size target: <300MB
- Include all Phase 3 dependencies (Cohere, MCP, FastAPI)

### FR-003: Kubernetes Deployments
- Frontend: 2 replicas, rolling update strategy
- Backend: 2 replicas, rolling update strategy
- Resource requests: 256Mi/250m CPU (frontend), 512Mi/500m CPU (backend)
- Resource limits: 512Mi/500m CPU (frontend), 1Gi/1000m CPU (backend)
- Liveness and readiness probes
- imagePullPolicy: Never (for Minikube local images)

### FR-004: Kubernetes Services
- Frontend Service: NodePort or LoadBalancer type
- Backend Service: ClusterIP type (internal only)
- Correct port mappings (80→3000 frontend, 8000→8000 backend)
- Proper selectors matching deployment labels

### FR-005: Configuration Management
- ConfigMap for: NODE_ENV, CORS_ORIGINS, API URLs
- Secrets for: COHERE_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET, JWT_SECRET
- All secrets base64 encoded
- Environment variables injected into pods

### FR-006: Helm Chart Structure
- Chart.yaml: name, version, description, appVersion
- values.yaml: default configuration (image names, tags, replicas, resources)
- templates/: all Kubernetes manifests as templates
- _helpers.tpl: template helper functions
- NOTES.txt: post-installation instructions

### FR-007: Networking
- Frontend accessible from host machine (Minikube service/tunnel)
- Backend only accessible within cluster
- Pod-to-pod communication via Kubernetes DNS
- Service names: frontend-service, backend-service
- Database accessible from pods (external URL)

### FR-008: Health & Monitoring
- Container logs via kubectl logs
- Resource usage via kubectl top
- Pod status monitoring
- Restart policy: Always
- Graceful shutdown handling

## Environment Variables:

### Frontend (in Kubernetes):
- NEXT_PUBLIC_API_URL=http://backend-service:8000
- NEXT_PUBLIC_APP_URL=http://localhost:3000
- COHERE_API_KEY (from secret)
- BETTER_AUTH_URL=http://localhost:3000
- BETTER_AUTH_SECRET (from secret)
- DATABASE_URL (from secret)
- JWT_SECRET (from secret)

### Backend (in Kubernetes):
- DATABASE_URL (from secret)
- COHERE_API_KEY (from secret)
- BETTER_AUTH_SECRET (from secret)
- JWT_SECRET (from secret)
- CORS_ORIGINS=http://localhost:3000

## Project Structure:
```
Phase-4/
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── (Phase 3 Next.js code)
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── (Phase 3 FastAPI code)
├── k8s/
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── configmap.yaml
│   └── secrets.yaml.example
├── helm-charts/
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── docker-compose.yml (for local testing)
└── README.md
```

## Testing Requirements:
- Docker images build successfully
- Containers run standalone (docker run test)
- docker-compose brings up full stack locally
- Kubernetes manifests apply without errors
- Helm chart installs successfully
- All pods reach Running state
- Health checks pass
- Frontend accessible from browser
- Backend API responds
- Authentication works
- All CRUD operations work
- Chatbot functional
- Database operations succeed

## Dependencies:
- Docker Desktop installed and running
- Minikube installed and started
- kubectl configured for Minikube context
- Helm 3 installed
- Phase 3 application code in Phase-4/
- Access to external Neon database
- Minimum 4GB RAM for Minikube
- 20GB free disk space

## Success Metrics:
- 100% Phase 3 features working in Kubernetes
- <5 minute deployment time with Helm
- Zero failed health checks
- Can scale to 5 replicas
- Rolling updates complete in <2 minutes

This specification guides containerization and Kubernetes deployment of Phase 3 todo application on local Minikube cluster.