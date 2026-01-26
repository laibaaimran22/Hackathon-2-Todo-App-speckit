# Phase 4: Local Kubernetes Deployment Implementation Plan

## Overview
This plan outlines the implementation of Phase 4, which involves containerizing the existing Phase 3 application (Next.js frontend + FastAPI backend + AI chatbot) and deploying it to a local Kubernetes cluster using Minikube, Docker, and Helm.

## Phase 4.1: Docker Containerization

### Tasks:
- Create frontend/Dockerfile with multi-stage build
- Create backend/Dockerfile with Python slim base
- Create frontend/.dockerignore
- Create backend/.dockerignore
- Create docker-compose.yml for local testing
- Build and test Docker images
- Optimize image sizes
- Verify standalone Next.js output works

### Deliverables:
- Phase-4/frontend/Dockerfile
- Phase-4/backend/Dockerfile
- Phase-4/frontend/.dockerignore
- Phase-4/backend/.dockerignore
- Phase-4/docker-compose.yml
- Working Docker images (<500MB frontend, <300MB backend)

### Success Criteria:
- ✅ Frontend image builds successfully (<500MB)
- ✅ Backend image builds successfully (<300MB)
- ✅ docker-compose starts full stack locally

## Phase 4.2: Kubernetes Manifests

### Tasks:
- Create frontend-deployment.yaml (2 replicas, health checks)
- Create backend-deployment.yaml (2 replicas, health checks)
- Create frontend-service.yaml (NodePort/LoadBalancer)
- Create backend-service.yaml (ClusterIP)
- Create configmap.yaml (non-sensitive config)
- Create secrets.yaml.example (template for secrets)
- Set resource limits and requests
- Configure liveness and readiness probes
- Test manifests with kubectl apply --dry-run

### Deliverables:
- Phase-4/k8s/frontend-deployment.yaml
- Phase-4/k8s/backend-deployment.yaml
- Phase-4/k8s/frontend-service.yaml
- Phase-4/k8s/backend-service.yaml
- Phase-4/k8s/configmap.yaml
- Phase-4/k8s/secrets.yaml.example

### Success Criteria:
- ✅ Kubernetes manifests apply without errors
- ✅ All manifests validated with dry-run

## Phase 4.3: Helm Chart Creation

### Tasks:
- Create Chart.yaml with metadata
- Create values.yaml with default configuration
- Create deployment templates for frontend/backend
- Create service templates for frontend/backend
- Create configmap template
- Create secrets template
- Create _helpers.tpl with common labels
- Create NOTES.txt with post-install instructions
- Test Helm chart with helm lint
- Package and test installation

### Deliverables:
- Phase-4/helm-charts/todo-app/Chart.yaml
- Phase-4/helm-charts/todo-app/values.yaml
- Phase-4/helm-charts/todo-app/templates/*.yaml
- Phase-4/helm-charts/todo-app/templates/_helpers.tpl
- Phase-4/helm-charts/todo-app/templates/NOTES.txt

### Success Criteria:
- ✅ Helm chart installs successfully
- ✅ Helm lint passes without errors

## Phase 4.4: Minikube Deployment

### Tasks:
- Start Minikube cluster with Docker driver
- Verify cluster is running
- Build Docker images for frontend and backend
- Load images into Minikube
- Create Kubernetes secrets with actual values
- Deploy application using Helm
- Verify all pods reach Running state
- Check services are created
- Get application URL
- Test access from browser

### Deliverables:
- Running Minikube cluster
- Images loaded in Minikube
- All pods Running (2 frontend, 2 backend)
- Services accessible
- Application working

### Success Criteria:
- ✅ All pods reach Running status (4 total: 2 frontend, 2 backend)
- ✅ Health checks pass
- ✅ Frontend accessible at localhost
- ✅ Backend API responds

## Phase 4.5: Testing & Documentation

### Tasks:
- Test all Phase 3 features in Kubernetes
- Test login and authentication
- Test add/edit/delete tasks
- Test chatbot functionality
- Test rolling updates (kubectl rollout)
- Test pod restarts and self-healing
- Test scaling (kubectl scale)
- Create comprehensive README
- Document troubleshooting steps
- Create kubectl commands cheat sheet
- Record demo video

### Deliverables:
- Phase-4/README.md (complete setup guide)
- Phase-4/TROUBLESHOOTING.md
- Phase-4/KUBECTL_COMMANDS.md
- All Phase 3 features verified working

### Success Criteria:
- ✅ Authentication works (login/signup)
- ✅ CRUD operations work (add/edit/delete/complete tasks)
- ✅ Chatbot functional
- ✅ Can scale pods: kubectl scale deployment frontend --replicas=3
- ✅ Rolling updates work: kubectl set image deployment/frontend frontend=todo-app-frontend:v2
- ✅ Logs accessible: kubectl logs -l app=frontend

## Technical Decisions

### Docker:
- Frontend base: node:20-alpine
- Backend base: python:3.11-slim
- Multi-stage builds for optimization
- Standalone Next.js output
- Non-root user in containers

### Kubernetes:
- 2 replicas per deployment
- Rolling update strategy (maxSurge: 1, maxUnavailable: 0)
- Resource requests and limits defined
- Health checks on /api/health (frontend) and /health (backend)
- imagePullPolicy: Never (for Minikube)

### Helm:
- Chart version: 0.1.0
- App version: 1.0.0
- Parameterized image tags
- Separate values files possible (values-dev.yaml, values-prod.yaml)

### Networking:
- Frontend: NodePort service (port 30080)
- Backend: ClusterIP service (internal only)
- Service names: frontend-service, backend-service
- Database: External Neon PostgreSQL

## Dependencies

### Prerequisites:
- Docker Desktop running
- Minikube started: minikube start --driver=docker
- kubectl configured for Minikube context
- Helm 3 installed
- 4GB RAM allocated to Minikube
- 20GB disk space available

### External Services:
- Neon PostgreSQL database (existing from Phase 3)
- Cohere API access (existing from Phase 3)

### Environment Variables:
- COHERE_API_KEY=your_cohere_api_key_here
- DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
- BETTER_AUTH_SECRET=your_auth_secret_here
- JWT_SECRET=your_jwt_secret_here

## Risks & Mitigation

### Risk: Docker images too large
**Mitigation**: Multi-stage builds, alpine base, .dockerignore

### Risk: Pods fail to start
**Mitigation**: Health checks, resource limits, proper dependencies

### Risk: Database connectivity issues
**Mitigation**: Test connection strings, verify network policies

### Risk: Environment variable mismatch
**Mitigation**: ConfigMaps, Secrets, clear documentation

### Risk: Image pull failures in Minikube
**Mitigation**: Use imagePullPolicy: Never, load images manually