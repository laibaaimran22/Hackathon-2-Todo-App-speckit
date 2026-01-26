# Troubleshooting Guide for Phase 4: Local Kubernetes Deployment

## Common Issues and Solutions

### 1. Minikube Not Starting

**Issue**: `minikube start` fails with driver errors
**Solution**:
```bash
# Check available drivers
minikube config get driver

# Set docker driver explicitly
minikube config set driver docker

# Start minikube
minikube start
```

### 2. Images Not Found in Minikube

**Issue**: Pods fail with `ErrImagePull` or `ImagePullBackOff`
**Solution**:
```bash
# Make sure images are built locally
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend

# Load images into minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 3. Secrets Not Working

**Issue**: Application fails to start due to missing secrets
**Solution**:
```bash
# Check if secrets exist
kubectl get secrets

# Create secrets with proper base64 encoding
kubectl create secret generic todo-app-secrets \
  --from-literal=database_url=$(echo -n "your-db-url" | base64) \
  --from-literal=cohere_api_key=$(echo -n "your-cohere-key" | base64) \
  --from-literal=better_auth_secret=$(echo -n "your-auth-secret" | base64) \
  --from-literal=jwt_secret=$(echo -n "your-jwt-secret" | base64)
```

### 4. Frontend Cannot Connect to Backend

**Issue**: Frontend shows errors connecting to backend API
**Solution**:
- Verify backend service is running: `kubectl get svc -l app=backend`
- Check service name matches what's in frontend env var: `NEXT_PUBLIC_API_URL=http://backend-service:8000`
- Verify pods can reach each other: `kubectl exec -it <frontend-pod> -- nslookup backend-service`

### 5. Port Not Accessible

**Issue**: Cannot access application on http://localhost:30080
**Solution**:
```bash
# Use minikube tunnel in a separate terminal
minikube tunnel

# Or get the service URL
minikube service <service-name> --url

# Check if NodePort is properly allocated
kubectl get svc
```

### 6. Database Connection Issues

**Issue**: Backend shows database connection errors
**Solution**:
- Verify DATABASE_URL is correctly set in secrets
- Check if external database is accessible from Minikube
- Verify database credentials and permissions
- Check firewall settings for Neon database

### 7. Health Checks Failing

**Issue**: Pods show as Unhealthy
**Solution**:
- Check if the health endpoints are accessible: `/api/health` for frontend, `/health` for backend
- Verify the application is listening on the correct port
- Adjust initial delay times if the application takes longer to start

### 8. Insufficient Resources

**Issue**: Pods stuck in Pending state
**Solution**:
```bash
# Check resource usage
kubectl top nodes
kubectl describe nodes

# Increase Minikube resources
minikube delete
minikube start --memory=4096 --cpus=2
```

### 9. Helm Installation Issues

**Issue**: Helm install fails
**Solution**:
```bash
# Check Helm status
helm list

# Check for errors
helm status <release-name>

# Uninstall and reinstall
helm uninstall <release-name>
helm install <release-name> .
```

## Debugging Commands

### Check Pod Status
```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs
```

### Check Services
```bash
kubectl get svc
kubectl describe svc <service-name>
```

### Check Deployments
```bash
kubectl get deployments
kubectl describe deployment <deployment-name>
```

### Exec into Pod
```bash
kubectl exec -it <pod-name> -- /bin/sh
```

### Check Events
```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

## Verifying Phase 3 Features Work

### Authentication
```bash
# Check auth endpoints are accessible
kubectl port-forward svc/<backend-service-name> 8000:8000
curl http://localhost:8000/api/auth/sign-in/email -X POST -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"password"}'
```

### CRUD Operations
```bash
# Test task creation
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/tasks -X POST -d '{"title":"Test","description":"Test"}'
```

### Database Connectivity
```bash
# Check if backend can connect to database
kubectl logs -l app=backend | grep -i "database\|error"
```

## Resource Limits

### Check Current Resource Usage
```bash
kubectl top pods
kubectl top nodes
```

### Check Resource Requests/Limits
```bash
kubectl describe pod <pod-name> | grep -A 10 Resources
```

## Network Issues

### Test Pod-to-Pod Communication
```bash
# Exec into frontend pod and test backend connectivity
kubectl exec -it <frontend-pod> -- ping backend-service
kubectl exec -it <frontend-pod> -- wget --spider backend-service:8000/health
```

### Check Service Discovery
```bash
kubectl exec -it <any-pod> -- nslookup <service-name>
```

## Rolling Updates

### If Update Fails
```bash
# Check rollout status
kubectl rollout status deployment/<deployment-name>

# Undo update
kubectl rollout undo deployment/<deployment-name>

# Check revision history
kubectl rollout history deployment/<deployment-name>
```