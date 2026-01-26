# Phase 4: Local Kubernetes Deployment

This Phase 4 implementation containerizes the Phase 3 Todo application and deploys it to a local Kubernetes cluster using Minikube, Docker, and Helm.

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

## Prerequisites

- Docker Desktop running
- Minikube installed and started: `minikube start --driver=docker`
- kubectl configured for Minikube context
- Helm 3 installed
- 4GB RAM allocated to Minikube
- 20GB disk space available
- Access to external Neon PostgreSQL database
- Access to Cohere API

## Setup Instructions

### 1. Start Minikube

```bash
minikube start --driver=docker
```

### 2. Build Docker Images

```bash
# Navigate to Phase-4 directory
cd Phase-4

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
cd ..

# Build backend image
cd backend
docker build -t todo-backend:latest .
cd ..
```

### 3. Load Images into Minikube

```bash
# Load images into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 4. Create Secrets

First, encode your secrets in base64:

```bash
# Encode your secrets
echo -n "your-database-url" | base64
echo -n "your-cohere-api-key" | base64
echo -n "your-better-auth-secret" | base64
echo -n "your-jwt-secret" | base64
```

Then create the Kubernetes secrets:

```bash
kubectl create secret generic todo-app-secrets \
  --from-literal=database_url="your-base64-encoded-database-url" \
  --from-literal=cohere_api_key="your-base64-encoded-cohere-api-key" \
  --from-literal=better_auth_secret="your-base64-encoded-better-auth-secret" \
  --from-literal=jwt_secret="your-base64-encoded-jwt-secret"
```

### 5. Deploy with Helm

```bash
cd helm-charts/todo-app
helm install todo-release .
```

### 6. Access the Application

```bash
# Get the service URL
minikube service todo-release-frontend-service --url
```

Or use `minikube tunnel` in a separate terminal and access `http://localhost:30080`

## Alternative: Deploy with kubectl

Instead of Helm, you can deploy directly with kubectl:

```bash
# Apply Kubernetes manifests
kubectl apply -f ../k8s/configmap.yaml
kubectl apply -f ../k8s/secrets.yaml  # Make sure secrets are created first
kubectl apply -f ../k8s/backend-deployment.yaml
kubectl apply -f ../k8s/backend-service.yaml
kubectl apply -f ../k8s/frontend-deployment.yaml
kubectl apply -f ../k8s/frontend-service.yaml
```

## Docker Compose for Local Testing

For local testing without Kubernetes:

```bash
# Set environment variables
export DATABASE_URL="your-database-url"
export COHERE_API_KEY="your-cohere-api-key"
export BETTER_AUTH_SECRET="your-better-auth-secret"
export JWT_SECRET="your-jwt-secret"

# Start with docker-compose
docker-compose up --build
```

## Scaling the Application

```bash
# Scale frontend pods
kubectl scale deployment todo-release-frontend --replicas=3

# Scale backend pods
kubectl scale deployment todo-release-backend --replicas=3
```

## Health Checks

The application includes health checks:
- Frontend: `/api/health` (exposed on port 3000)
- Backend: `/health` (exposed on port 8000)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

## Useful Commands

See [KUBECTL_COMMANDS.md](KUBECTL_COMMANDS.md) for common kubectl commands.