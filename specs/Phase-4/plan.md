# Phase 4: Local Kubernetes Deployment Implementation Plan

## Overview
Detailed implementation plan for containerizing the Phase 3 todo application and deploying it to a local Kubernetes cluster using Minikube.

## Context
- Phase-4/ folder is duplicate of Phase-3/ with working Next.js + FastAPI + AI chatbot
- Need to add Docker containerization and Kubernetes deployment
- Deploy to local Minikube cluster
- All specifications in specs/Phase-4/
- Implementation happens in Phase-4/ folder

## Deliverables

### Phase 4.1: Docker Containerization
- [ ] Create Dockerfile for Next.js frontend
- [ ] Create Dockerfile for FastAPI backend
- [ ] Create .dockerignore files
- [ ] Create docker-compose.yml for local testing
- [ ] Build and test Docker images locally
- [ ] Optimize image sizes

### Phase 4.2: Kubernetes Manifests
- [ ] Create frontend-deployment.yaml
- [ ] Create backend-deployment.yaml
- [ ] Create frontend-service.yaml
- [ ] Create backend-service.yaml
- [ ] Create configmap.yaml
- [ ] Create secrets.yaml.example
- [ ] Test manifests with kubectl apply

### Phase 4.3: Helm Chart Creation
- [ ] Create Chart.yaml with metadata
- [ ] Create values.yaml with configuration
- [ ] Create template files for all resources
- [ ] Create helper templates (_helpers.tpl)
- [ ] Create NOTES.txt with post-install instructions
- [ ] Package and test Helm chart

### Phase 4.4: Minikube Deployment
- [ ] Start Minikube cluster
- [ ] Build Docker images
- [ ] Load images into Minikube
- [ ] Create Kubernetes secrets
- [ ] Install application using Helm
- [ ] Verify all pods running
- [ ] Test application functionality

### Phase 4.5: Testing & Documentation
- [ ] Test all Phase 3 features in Kubernetes
- [ ] Test rolling updates
- [ ] Test pod restarts
- [ ] Create README with setup instructions
- [ ] Document troubleshooting steps
- [ ] Create kubectl commands cheat sheet

## Files to Create

### Phase-4/frontend/
- [ ] Dockerfile
- [ ] .dockerignore

### Phase-4/backend/
- [ ] .dockerignore (if not exists)

### Phase-4/k8s/
- [ ] frontend-deployment.yaml
- [ ] backend-deployment.yaml
- [ ] frontend-service.yaml
- [ ] backend-service.yaml
- [ ] configmap.yaml
- [ ] secrets.yaml.example

### Phase-4/helm-charts/todo-app/
- [ ] Chart.yaml
- [ ] values.yaml
- [ ] templates/
  - [ ] deployment-frontend.yaml
  - [ ] deployment-backend.yaml
  - [ ] service-frontend.yaml
  - [ ] service-backend.yaml
  - [ ] configmap.yaml
  - [ ] secrets.yaml
  - [ ] _helpers.tpl
  - [ ] NOTES.txt

### Phase-4/
- [ ] docker-compose.yml (enhanced)
- [ ] Makefile
- [ ] README.md

## Technical Decisions

### Docker:
- Use multi-stage builds for smaller images
- Node.js base: node:18-alpine
- Python base: python:3.11-slim
- Non-root user in containers

### Kubernetes:
- 2 replicas per deployment
- Rolling update strategy
- Resource limits: 512Mi RAM, 500m CPU (frontend)
- Resource limits: 1Gi RAM, 1000m CPU (backend)
- Health checks on /api/health and /health

### Helm:
- Chart version: 0.1.0
- App version: 1.0.0
- Parameterized image tags
- Separate values files for environments

### Networking:
- Frontend: NodePort service (port 30080)
- Backend: ClusterIP service (internal)
- Database: External Neon PostgreSQL

## Dependencies

### Prerequisites:
- Docker Desktop running
- Minikube started (minikube start)
- kubectl configured
- Helm 3 installed
- 4GB RAM allocated to Minikube
- 20GB disk space available

### External Services:
- Neon PostgreSQL database
- Cohere API access

## Implementation Steps

### Step 1: Docker Containerization
1. Create Dockerfile for frontend with multi-stage build
2. Create .dockerignore for frontend
3. Enhance existing backend Dockerfile if needed
4. Create .dockerignore for backend
5. Update docker-compose.yml for both services
6. Test local builds

### Step 2: Kubernetes Manifests
1. Create namespace for the application
2. Create ConfigMap with non-sensitive config
3. Create Secret template/example
4. Create backend deployment with 2 replicas
5. Create backend service (ClusterIP)
6. Create frontend deployment with 2 replicas
7. Create frontend service (NodePort)
8. Apply and test manifests

### Step 3: Helm Chart
1. Initialize Helm chart structure
2. Create values.yaml with defaults
3. Convert Kubernetes manifests to Helm templates
4. Add helper functions in _helpers.tpl
5. Create NOTES.txt with post-install instructions
6. Test Helm install/uninstall

### Step 4: Minikube Deployment
1. Start Minikube with adequate resources
2. Configure Docker to use Minikube registry
3. Build and push images to Minikube
4. Create required secrets in Minikube
5. Install Helm chart
6. Verify deployment status

### Step 5: Testing and Documentation
1. Test all Phase 3 features in Kubernetes
2. Verify health checks are working
3. Test scaling and rolling updates
4. Document the setup process
5. Create troubleshooting guide

## Success Criteria

After implementation:
- [ ] Frontend image builds (<500MB)
- [ ] Backend image builds (<300MB)
- [ ] docker-compose starts full stack
- [ ] Kubernetes manifests apply successfully
- [ ] Helm chart installs without errors
- [ ] All pods reach Running status
- [ ] Health checks pass
- [ ] Frontend accessible at localhost
- [ ] Backend API responds
- [ ] Authentication works
- [ ] CRUD operations work
- [ ] Chatbot functional
- [ ] Can scale pods with kubectl scale
- [ ] Rolling updates work

## Risks & Mitigation

### Risk: Docker images too large
- **Mitigation**: Multi-stage builds, .dockerignore, alpine base images

### Risk: Pods fail to start
- **Mitigation**: Proper health checks, resource limits, dependency ordering

### Risk: Database connectivity issues
- **Mitigation**: Test connection strings, network policies, secrets management

### Risk: Environment variable mismatch
- **Mitigation**: ConfigMaps, Secrets, clear documentation

## Rollback Plan
If deployment fails:
1. Uninstall Helm release: `helm uninstall todo-app`
2. Delete namespace if created manually
3. Revert Docker images to previous versions if needed
4. Restore original docker-compose.yml if modified

## Timeline
- Docker Containerization: 1 day
- Kubernetes Manifests: 1 day
- Helm Chart Creation: 1 day
- Minikube Deployment: 1 day
- Testing & Documentation: 1 day
- Total estimated time: 5 days