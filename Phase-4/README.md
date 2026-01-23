# Phase 4: Local Kubernetes Deployment

This project implements the containerization and Kubernetes deployment of the Todo application using Docker, Kubernetes, and Helm.

## Architecture
```
localhost → Minikube Service → Frontend Pod → Backend Service → Backend Pod → Neon DB
```

## Prerequisites
- Docker Desktop running
- Minikube started (`minikube start`)
- kubectl configured
- Helm 3 installed
- 4GB RAM allocated to Minikube
- 20GB disk space available

## Quick Start

### Local Development with Docker Compose
```bash
cd Phase-4
docker-compose up --build
```

### Kubernetes Deployment with Helm

1. Start Minikube:
```bash
minikube start --memory=4096 --cpus=2
```

2. Enable ingress addon (optional):
```bash
minikube addons enable ingress
```

3. Build and load Docker images into Minikube:
```bash
eval $(minikube docker-env)
docker build -t frontend:latest ./frontend
docker build -t backend:latest ./backend
```

4. Create Kubernetes secrets:
```bash
kubectl create secret generic todo-app-secrets \
  --from-literal=database-url=$(echo -n '<your-encoded-database-url>' | base64) \
  --from-literal=jwt-secret=$(echo -n '<your-encoded-jwt-secret>' | base64) \
  --from-literal=auth-secret=$(echo -n '<your-encoded-auth-secret>' | base64) \
  --from-literal=cohere-api-key=$(echo -n '<your-encoded-cohere-api-key>' | base64)
```

5. Install the application using Helm:
```bash
cd helm-charts/todo-app
helm install todo-app .
```

6. Access the application:
```bash
minikube service todo-app-frontend --url
```

## Kubernetes Resources

The deployment creates the following resources:
- Frontend Deployment (2 replicas)
- Backend Deployment (2 replicas)
- Frontend Service (NodePort)
- Backend Service (ClusterIP)
- ConfigMap for non-sensitive configuration
- Secret for sensitive data

## Helm Chart Configuration

The Helm chart is located in `helm-charts/todo-app/` and can be customized using values in `values.yaml`.

### Custom Values Example
Create a `custom-values.yaml` file:
```yaml
replicaCount:
  frontend: 3
  backend: 3

image:
  frontend:
    tag: v1.0.0
  backend:
    tag: v1.0.0

service:
  frontend:
    nodePort: 30081
```

Then install with custom values:
```bash
helm install todo-app . -f custom-values.yaml
```

## Development Commands

### Using Makefile
```bash
make build-images          # Build Docker images
make deploy-minikube       # Deploy to Minikube
make undeploy-minikube     # Remove deployment from Minikube
make test-deployment       # Test the deployment
make logs-frontend         # View frontend logs
make logs-backend          # View backend logs
```

### Direct kubectl Commands
```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# View logs
kubectl logs -l app=frontend
kubectl logs -l app=backend

# Scale deployments
kubectl scale deployment todo-app-frontend --replicas=3
kubectl scale deployment todo-app-backend --replicas=3

# Port forward for local testing
kubectl port-forward svc/todo-app-frontend 3000:3000
kubectl port-forward svc/todo-app-backend 8000:8000
```

## Troubleshooting

### Common Issues
1. **Images not found**: Make sure to run `eval $(minikube docker-env)` before building images
2. **Database connection issues**: Verify that secrets are properly encoded and set
3. **Service not accessible**: Check that the NodePort is available and not blocked by firewall

### Useful Commands
```bash
# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Describe resources for detailed information
kubectl describe pod <pod-name>
kubectl describe service <service-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

## Health Checks

- Frontend: Available at `/` and `/api/health`
- Backend: Available at `/health`

Both services have liveness and readiness probes configured.

## Scaling

The application supports horizontal pod autoscaling. You can manually scale deployments:

```bash
kubectl scale deployment todo-app-frontend --replicas=5
kubectl scale deployment todo-app-backend --replicas=5
```

## Cleanup

To remove the deployment:
```bash
helm uninstall todo-app
kubectl delete secret todo-app-secrets
```