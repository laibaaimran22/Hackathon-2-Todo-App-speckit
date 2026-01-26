# Kubernetes Commands Reference for Todo Application

## Basic Commands

### Get Resources
```bash
# Get all pods
kubectl get pods

# Get pods with labels
kubectl get pods --show-labels

# Get services
kubectl get svc

# Get deployments
kubectl get deployments

# Get configmaps
kubectl get configmaps

# Get secrets
kubectl get secrets

# Get all resources in one command
kubectl get all
```

### Describe Resources
```bash
# Describe a pod (get detailed information)
kubectl describe pod <pod-name>

# Describe a service
kubectl describe svc <service-name>

# Describe a deployment
kubectl describe deployment <deployment-name>

# Describe a configmap
kubectl describe configmap <configmap-name>

# Describe a secret
kubectl describe secret <secret-name>
```

## Logging and Monitoring

### View Logs
```bash
# View logs from a pod
kubectl logs <pod-name>

# View logs from all pods with a label
kubectl logs -l app=frontend

# Follow logs in real-time
kubectl logs -f <pod-name>

# View logs from previous terminated container
kubectl logs --previous <pod-name>

# Tail last 20 lines of logs
kubectl logs --tail=20 <pod-name>
```

### Resource Usage
```bash
# Get resource usage of nodes
kubectl top nodes

# Get resource usage of pods
kubectl top pods

# Get resource usage of specific pod
kubectl top pod <pod-name>
```

## Managing Deployments

### Scaling
```bash
# Scale a deployment to 3 replicas
kubectl scale deployment <deployment-name> --replicas=3

# Scale frontend deployment
kubectl scale deployment todo-release-frontend --replicas=3

# Scale backend deployment
kubectl scale deployment todo-release-backend --replicas=3
```

### Rolling Updates
```bash
# Update image in deployment
kubectl set image deployment/<deployment-name> <container-name>=<new-image>:<tag>

# Example: Update frontend image
kubectl set image deployment/todo-release-frontend frontend=todo-frontend:v2

# Check rollout status
kubectl rollout status deployment/<deployment-name>

# View rollout history
kubectl rollout history deployment/<deployment-name>

# Undo rollout
kubectl rollout undo deployment/<deployment-name>

# Undo to specific revision
kubectl rollout undo deployment/<deployment-name> --to-revision=2
```

## Pod Management

### Exec into Pod
```bash
# Execute command in pod
kubectl exec <pod-name> -- <command>

# Interactive shell in pod
kubectl exec -it <pod-name> -- /bin/sh

# Execute command in specific container (if multiple containers in pod)
kubectl exec <pod-name> -c <container-name> -- <command>
```

### Port Forwarding
```bash
# Forward local port to pod port
kubectl port-forward <pod-name> <local-port>:<pod-port>

# Forward to service
kubectl port-forward svc/<service-name> <local-port>:<service-port>

# Example: Access backend locally
kubectl port-forward svc/todo-release-backend-service 8000:8000
```

## Service Management

### Access Services
```bash
# Get service external IP/URL
kubectl get svc

# Get specific service details
kubectl get svc <service-name> -o wide

# Get service as JSON
kubectl get svc <service-name> -o json

# Get service as YAML
kubectl get svc <service-name> -o yaml
```

## Debugging

### Troubleshooting Commands
```bash
# Get events
kubectl get events

# Get events sorted by timestamp
kubectl get events --sort-by=.metadata.creationTimestamp

# Get events for specific namespace
kubectl get events -n <namespace>

# Get detailed pod status
kubectl describe pod <pod-name>

# Check if pod is running and ready
kubectl get pods -w  # Watch continuously

# Get pod IP
kubectl get pod <pod-name> -o jsonpath='{.status.podIP}'
```

## Namespaces

### Working with Namespaces
```bash
# Get all namespaces
kubectl get namespaces

# Use specific namespace for commands
kubectl get pods -n <namespace>

# Set default namespace
kubectl config set-context --current --namespace=<namespace>

# Create namespace
kubectl create namespace <namespace-name>

# Get resources in all namespaces
kubectl get pods --all-namespaces
```

## ConfigMaps and Secrets

### Manage ConfigMaps
```bash
# Create configmap from literal values
kubectl create configmap <configmap-name> --from-literal=key1=value1 --from-literal=key2=value2

# Create configmap from file
kubectl create configmap <configmap-name> --from-file=<path-to-file>

# Get configmap
kubectl get configmap <configmap-name> -o yaml

# Edit configmap
kubectl edit configmap <configmap-name>
```

### Manage Secrets
```bash
# Create secret from literal values
kubectl create secret generic <secret-name> --from-literal=key1=value1 --from-literal=key2=value2

# Create secret from file
kubectl create secret generic <secret-name> --from-file=<path-to-file>

# Get secret (will show base64 encoded values)
kubectl get secret <secret-name> -o yaml

# Decode a secret value
kubectl get secret <secret-name> -o jsonpath='{.data.key1}' | base64 -d
```

## Label and Annotation Management

### Working with Labels
```bash
# Get resources with specific label
kubectl get pods -l app=frontend

# Add label to resource
kubectl label pod <pod-name> key=value

# Remove label
kubectl label pod <pod-name> key-

# Get resources with label containing partial match
kubectl get pods -l 'app in (frontend,backend)'
```

### Working with Annotations
```bash
# Add annotation to resource
kubectl annotate pod <pod-name> key=value

# Remove annotation
kubectl annotate pod <pod-name> key-
```

## Cleanup

### Delete Resources
```bash
# Delete pod
kubectl delete pod <pod-name>

# Delete deployment
kubectl delete deployment <deployment-name>

# Delete service
kubectl delete svc <service-name>

# Delete configmap
kubectl delete configmap <configmap-name>

# Delete secret
kubectl delete secret <secret-name>

# Delete all resources with specific label
kubectl delete all -l app=frontend

# Delete everything in namespace
kubectl delete all --all -n <namespace>
```

## Useful Shortcuts

### Resource Abbreviations
- `po` for `pods`
- `svc` for `services`
- `deploy` for `deployments`
- `cm` for `configmaps`
- `sec` for `secrets`
- `ns` for `namespaces`

### Examples:
```bash
kubectl get po
kubectl get svc
kubectl get deploy
kubectl describe po <pod-name>
```

## Helm Integration

### Helm Commands with Kubectl
```bash
# Get resources created by a Helm release
kubectl get all -l app.kubernetes.io/instance=<release-name>

# Get Helm release status
helm status <release-name>

# List Helm releases
helm list

# Check if Helm release exists
kubectl get all -l app.kubernetes.io/instance=todo-release
```

These commands will help you manage and troubleshoot your Todo application running in Kubernetes.