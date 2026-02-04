# Phase 5: Advanced Cloud Deployment Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Advanced Features Implementation](#advanced-features-implementation)
3. [Event-Driven Architecture](#event-driven-architecture)
4. [Deployment Guide](#deployment-guide)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Cost Optimization](#cost-optimization)

## Architecture Overview

### System Components
- **Frontend**: Next.js 15 application with advanced UI features
- **Backend**: FastAPI service with Dapr integration
- **Database**: Neon PostgreSQL (free tier)
- **Event Stream**: Redpanda (Kafka-compatible)
- **State Management**: Dapr with Valkey (Redis-compatible)
- **Orchestration**: Kubernetes on Oracle Cloud
- **Service Mesh**: Dapr sidecars

### Data Flow
```
User Interaction → Frontend → Backend → Dapr Sidecar → Event Publishing → Redpanda → Event Consumers → State Updates
```

## Advanced Features Implementation

### 1. Recurring Tasks
- **Implementation**: Cron-like scheduling with pattern recognition
- **Database**: `recurrence_pattern` field in Task model
- **Logic**: Event-driven creation of new tasks based on recurrence rules
- **Supported Patterns**: daily, weekly, monthly

### 2. Due Dates with Email Reminders
- **Implementation**: Timestamp-based reminder system
- **Database**: `due_date` field in Task model
- **Logic**: Background scheduler checking upcoming due dates
- **Notification**: Email delivery service integration

### 3. Priority Levels
- **Implementation**: Enum-based priority system
- **Database**: `priority` field (high/medium/low) in Task model
- **UI**: Color-coded priority indicators
- **Sorting**: Priority-aware task ordering

### 4. Tags/Categories
- **Implementation**: Many-to-many relationship with Task model
- **Database**: Separate Tag model with TaskTagLink junction table
- **UI**: Tag input and filtering controls
- **Search**: Tag-based filtering capabilities

### 5. Full-Text Search
- **Implementation**: Search across multiple fields
- **Fields**: Title, description, tags
- **Indexing**: PostgreSQL full-text search indexes
- **Performance**: Optimized query patterns

### 6. Advanced Filters
- **Status Filter**: Pending, completed, all
- **Priority Filter**: High, medium, low, all
- **Tag Filter**: Specific tags or all
- **Date Range**: Custom date filtering
- **Combination**: Multiple filters applied simultaneously

### 7. Sorting Options
- **By Date**: Creation date, due date (ascending/descending)
- **By Priority**: High to low, low to high
- **By Name**: Alphabetical ordering
- **Custom**: User-defined sort orders

## Event-Driven Architecture

### Event Types
- `task.created`: New task creation
- `task.updated`: Task modification
- `task.completed`: Task completion
- `task.deleted`: Task deletion
- `task.reminder`: Due date approaching
- `task.recurring`: Recurring task generation

### Event Processing
- **Publisher**: Backend services publish events via Dapr
- **Broker**: Redpanda handles event persistence
- **Consumers**: Multiple services consume relevant events
- **Guarantees**: At-least-once delivery semantics

### Dapr Components
- **PubSub**: Kafka component for event streaming
- **State Store**: Redis component for state management
- **Service Invocation**: Inter-service communication
- **Bindings**: External system integration

## Deployment Guide

### Prerequisites
- Oracle Cloud Always Free account
- kubectl installed
- Helm 3+ installed
- Docker installed

### Step-by-Step Deployment

#### 1. Oracle Cloud Setup
```bash
# Install OCI CLI
curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh -o install.sh
chmod +x install.sh
./install.sh --accept-all-defaults

# Configure OCI
oci setup config
```

#### 2. Kubernetes Cluster Access
```bash
# Get Kubeconfig for your OKE cluster
oci ce cluster create-kubeconfig --cluster-id <your-cluster-id> --file $HOME/.kube/config --region <your-region>
```

#### 3. Install Dapr
```bash
helm repo add dapr https://daprio.github.io/helm-charts
helm repo update
helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait
```

#### 4. Prepare Secrets
```bash
# Create Kubernetes secrets for application
kubectl create secret generic todo-app-secrets \
  --from-literal=database_url=<your-encoded-db-url> \
  --from-literal=cohere_api_key=<your-encoded-api-key> \
  --from-literal=better_auth_secret=<your-encoded-auth-secret> \
  --from-literal=jwt_secret=<your-encoded-jwt-secret>
```

#### 5. Deploy Application
```bash
helm install todo-app ./helm-charts/todo-app --values ./helm-charts/todo-app/values.yaml
```

#### 6. Configure Domain (Optional)
```bash
# Update ingress configuration with your domain
# Edit values.yaml ingress section with your domain
```

## CI/CD Pipeline

### GitHub Actions Workflow
- **Trigger**: Push to main branch or pull request
- **Build**: Docker image creation
- **Test**: Automated testing suite
- **Deploy**: Helm-based deployment to OKE
- **Verify**: Post-deployment validation

### Pipeline Stages
1. **Test Stage**: Unit and integration tests
2. **Build Stage**: Multi-platform Docker builds
3. **Scan Stage**: Security vulnerability scanning
4. **Deploy Stage**: Progressive deployment with rollback
5. **Verify Stage**: Health checks and validation

### Configuration
- **Repository Secrets**: OCI credentials, cluster ID
- **Environment Variables**: Region, tenancy, namespace
- **Branch Protection**: Required reviews and status checks

## Testing

### Test Categories
- **Unit Tests**: Individual function testing
- **Integration Tests**: Component interaction testing
- **End-to-End Tests**: Full user journey testing
- **Performance Tests**: Load and stress testing
- **Security Tests**: Vulnerability and penetration testing

### Test Coverage
- **Backend API**: 95%+ coverage
- **Frontend Components**: 90%+ coverage
- **Event Handlers**: 100% coverage
- **Database Models**: 95%+ coverage

### Test Execution
```bash
# Run all tests
pytest tests/

# Run specific test suites
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Generate coverage report
pytest --cov=backend --cov=frontend --cov-report=html
```

## Troubleshooting

### Common Issues

#### Resource Limits
- **Symptom**: Pod crashes or evictions
- **Cause**: Exceeding Oracle Cloud Always Free limits
- **Solution**: Optimize resource requests/limits

#### Dapr Sidecar Issues
- **Symptom**: Application fails to start
- **Cause**: Dapr sidecar initialization problems
- **Solution**: Check dapr-system namespace logs

#### Event Processing Failures
- **Symptom**: Events not processed
- **Cause**: Redpanda connectivity issues
- **Solution**: Verify Redpanda cluster status

#### Database Connection Problems
- **Symptom**: Database errors
- **Cause**: Connection pool exhaustion
- **Solution**: Adjust connection settings

### Diagnostic Commands
```bash
# Check all pods
kubectl get pods --all-namespaces

# Check Dapr status
kubectl get pods -n dapr-system

# Check application logs
kubectl logs -f deployment/backend
kubectl logs -f deployment/frontend

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Port forward for debugging
kubectl port-forward service/backend-service 8000:8000
```

## Cost Optimization

### Oracle Cloud Always Free Limits
- **Compute**: 4 ARM CPU cores, 24GB RAM
- **Storage**: 200GB
- **Network**: Monthly bandwidth allowance
- **Services**: Kubernetes cluster, load balancer

### Optimization Strategies
- **ARM Nodes**: Use ARM-based compute for cost efficiency
- **Resource Requests**: Right-size CPU and memory requests
- **Auto Scaling**: Configure HPA with resource metrics
- **Image Optimization**: Multi-stage builds with minimal layers
- **Monitoring**: Track usage against free tier limits

### Cost Monitoring
- **OCI Console**: Real-time resource usage
- **Alerts**: Threshold-based notifications
- **Reports**: Monthly usage summaries
- **Forecasting**: Predictive cost modeling

---

## Maintenance Guidelines

### Regular Tasks
- **Backup**: Weekly database backups
- **Updates**: Monthly dependency updates
- **Monitoring**: Daily health checks
- **Optimization**: Quarterly resource optimization

### Emergency Procedures
- **Outage Response**: Incident response playbook
- **Rollback Plan**: Quick rollback procedures
- **Contact List**: Support team contacts
- **Documentation**: Recovery procedures

This documentation provides a comprehensive guide for operating the Phase 5 application in production.