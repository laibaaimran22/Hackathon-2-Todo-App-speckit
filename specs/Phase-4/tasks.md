# Phase 4: Local Kubernetes Deployment - Tasks

## Overview
Complete task list for containerizing the Phase 3 todo application and deploying it to a local Kubernetes cluster using Minikube.

## Phase 4.1: Docker Containerization
- [x] Create Dockerfile for Next.js frontend
- [x] Create Dockerfile for FastAPI backend
- [x] Create .dockerignore files
- [x] Create docker-compose.yml for local testing
- [x] Build and test Docker images locally
- [x] Optimize image sizes

## Phase 4.2: Kubernetes Manifests
- [x] Create frontend-deployment.yaml
- [x] Create backend-deployment.yaml
- [x] Create frontend-service.yaml
- [x] Create backend-service.yaml
- [x] Create configmap.yaml
- [x] Create secrets.yaml.example
- [x] Test manifests with kubectl apply

## Phase 4.3: Helm Chart Creation
- [x] Create Chart.yaml with metadata
- [x] Create values.yaml with configuration
- [x] Create template files for all resources
- [x] Create helper templates (_helpers.tpl)
- [x] Create NOTES.txt with post-install instructions
- [x] Package and test Helm chart

## Phase 4.4: Minikube Deployment
- [x] Start Minikube cluster
- [x] Build Docker images
- [x] Load images into Minikube
- [x] Create Kubernetes secrets
- [x] Install application using Helm
- [x] Verify all pods running
- [x] Test application functionality

## Phase 4.5: Testing & Documentation
- [x] Test all Phase 3 features in Kubernetes
- [x] Test rolling updates
- [x] Test pod restarts
- [x] Create README with setup instructions
- [x] Document troubleshooting steps
- [x] Create kubectl commands cheat sheet

## Technical Requirements
- Use multi-stage builds for smaller images
- Node.js base: node:18-alpine
- Python base: python:3.11-slim
- Non-root user in containers
- 2 replicas per deployment
- Rolling update strategy
- Resource limits: 512Mi RAM, 500m CPU (frontend)
- Resource limits: 1Gi RAM, 1000m CPU (backend)
- Health checks on /api/health and /health
- Chart version: 0.1.0
- App version: 1.0.0
- Parameterized image tags
- Frontend: NodePort service (port 30080)
- Backend: ClusterIP service (internal)
- Database: External Neon PostgreSQL

## Success Criteria
- [x] Frontend image builds (<500MB)
- [x] Backend image builds (<300MB)
- [x] docker-compose starts full stack
- [x] Kubernetes manifests apply successfully
- [x] Helm chart installs without errors
- [x] All pods reach Running status
- [x] Health checks pass
- [x] Frontend accessible at localhost
- [x] Backend API responds
- [x] Authentication works
- [x] CRUD operations work
- [x] Chatbot functional
- [x] Can scale pods with kubectl scale
- [x] Rolling updates work