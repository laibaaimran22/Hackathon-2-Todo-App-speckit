# Phase 4: Local Kubernetes Deployment

## Overview
Phase 4 focuses on containerizing the Phase 3 todo application and deploying it to a local Kubernetes cluster using Minikube. This phase adds Docker and Kubernetes deployment capabilities while maintaining all existing functionality.

## Target Audience
DevOps engineers containerizing and deploying Phase 3 todo application to local Kubernetes

## Focus
Dockerize Next.js frontend and FastAPI backend, create Kubernetes manifests, package with Helm, deploy to Minikube cluster

## Success Criteria
- Frontend and backend running in Kubernetes pods
- All Phase 3 features working (auth, CRUD, chatbot)
- Application accessible via localhost
- Helm chart successfully deploys entire stack
- Docker images optimized (<500MB frontend, <300MB backend)
- Zero-downtime rolling updates possible
- Health checks and readiness probes working

## Constraints
- Working Directory: Phase-4/ (duplicate of Phase-3/)
- Specifications: specs/Phase-4/
- History: history/Phase-4/
- Technology: Docker, Kubernetes, Helm, Minikube
- Deployment: Local Kubernetes (Minikube) ONLY
- Database: External Neon PostgreSQL (not containerized)
- Must maintain ALL Phase 3 functionality
- Timeline: Complete by Phase 4 deadline

## Key Components to Build

### 1. Docker Containerization:
- Frontend Dockerfile (Next.js)
- Backend Dockerfile (FastAPI)
- Multi-stage builds
- .dockerignore files
- docker-compose.yml for testing

### 2. Kubernetes Manifests:
- Frontend Deployment (2 replicas)
- Backend Deployment (2 replicas)
- Frontend Service (NodePort/LoadBalancer)
- Backend Service (ClusterIP)
- ConfigMap (non-sensitive config)
- Secrets (API keys, database URL)

### 3. Helm Chart:
- Chart.yaml
- values.yaml
- Templates for all resources
- Parameterized configuration

### 4. Deployment:
- Build images
- Load into Minikube
- Deploy with Helm
- Access via localhost

## Architecture:
localhost → Minikube Service → Frontend Pod → Backend Service → Backend Pod → Neon DB

## Functional Requirements:

### FR-001: Dockerize Frontend
- Multi-stage Dockerfile
- Optimized image size
- Environment variables via ConfigMap
- Port 3000 exposed
- Health check endpoint

### FR-002: Dockerize Backend
- Python slim base image
- Production dependencies only
- Non-root user
- Port 8000 exposed
- Health check endpoint

### FR-003: Kubernetes Resources
- Deployments with 2 replicas each
- Services for networking
- ConfigMaps for config
- Secrets for sensitive data
- Resource limits and requests

### FR-004: Helm Chart
- Package all Kubernetes resources
- Parameterized values
- Easy installation command
- Post-install notes

### FR-005: Local Deployment
- Build and load images to Minikube
- Install via Helm
- Verify all pods running
- Access application locally

## Environment Variables:
- COHERE_API_KEY (secret)
- DATABASE_URL (secret)
- BETTER_AUTH_SECRET (secret)
- JWT_SECRET (secret)
- CORS_ORIGINS (configmap)
- API URLs (configmap)

## Testing:
- Docker images build successfully
- Pods reach Running state
- Health checks pass
- All Phase 3 features work

## Not Building:
- Cloud deployment (Phase 5)
- Database containerization
- CI/CD pipelines
- Monitoring stack
- Auto-scaling

## Dependencies:
- Docker Desktop running
- Minikube started
- kubectl configured
- Helm installed
- Phase 3 code in Phase-4/
- External Neon database access

## All Phase 3 Features Work:
- Authentication functional
- CRUD operations work
- Chatbot functional