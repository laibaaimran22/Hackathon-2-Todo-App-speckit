# Phase 5: Advanced Cloud Deployment (100% Free)

## Overview
This phase deploys the Todo Evolution application to Oracle Cloud Always Free tier with advanced features and event-driven architecture using Kubernetes, Dapr, and Redpanda. All components operate within 100% free tier limits with zero monthly costs.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │────│   Load Balancer  │────│   Internet      │
│   (Next.js)     │    │   (OCI)          │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Backend       │────│   Dapr Sidecar   │────│   Redpanda      │
│   (FastAPI)     │    │   (Service Mesh) │    │   (Events)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
┌─────────────────┐    ┌──────────────────┐
│   Database      │    │   Valkey         │
│   (Neon PG)     │    │   (Cache)        │
└─────────────────┘    └──────────────────┘
```

## Features Implemented

### 1. Recurring Tasks
- Support daily, weekly, monthly recurring patterns
- Background job processor for recurring tasks

### 2. Due Dates with Email Reminders
- Task due date field with timezone support
- Email notification system for reminders

### 3. Priority Levels
- High/Medium/Low priority classification
- Priority-based sorting and filtering

### 4. Tags/Categories
- User-defined tags for tasks
- Multi-tag assignment per task
- Tag-based filtering and grouping

### 5. Full-Text Search
- Search across task titles, descriptions, tags
- Real-time search suggestions

### 6. Advanced Filters
- Filter by status (pending, in-progress, completed)
- Filter by priority levels
- Filter by tags/categories
- Date range filtering
- Combined filter combinations

### 7. Sorting Options
- Sort by creation date, due date
- Sort by priority level
- Sort by task name/alphabetically
- Custom sort orders

## Technology Stack

### Infrastructure
- **Oracle Cloud Always Free**: Account with email + phone verification (no credit card)
- **Oracle Kubernetes Engine (OKE)**: Managed Kubernetes cluster
- **Oracle Container Registry**: Free container image hosting
- **Load Balancer**: Traffic distribution

### Application Runtime
- **Dapr**: Distributed Application Runtime for microservices
- **Redpanda**: Kafka-compatible event streaming platform
- **Valkey**: Redis-compatible in-memory datastore

### Application Components
- **Next.js 15**: Frontend framework
- **FastAPI**: Backend API framework
- **PostgreSQL**: Neon PostgreSQL (free tier)
- **Docker**: Containerization

## Event-Driven Architecture

### Event Types
- `task.created`: New task created
- `task.updated`: Task modified
- `task.completed`: Task marked as completed
- `task.reminder`: Due date reminder triggered
- `task.recurring`: Recurring task generation

### Event Processing Flow
1. Frontend creates/modifies tasks via API
2. Backend publishes events to Redpanda via Dapr
3. Event consumers subscribe to relevant topics
4. Background processors handle business logic
5. State updates published back to Dapr state stores

## Deployment

### Prerequisites
- Oracle Cloud Always Free account (email + phone only, NO credit card)
- Oracle Cloud CLI installed
- kubectl installed
- Helm installed

### Setup Steps

#### 1. Clone Repository
```bash
git clone <repository-url>
cd Phase-5
```

#### 2. Set Up Oracle Cloud CLI
```bash
# Install OCI CLI
curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh -o install.sh
chmod +x install.sh
./install.sh --accept-all-defaults

# Configure OCI CLI
oci setup config
```

#### 3. Get Kubeconfig for OKE Cluster
```bash
oci ce cluster create-kubeconfig --cluster-id <your-cluster-id> --file $HOME/.kube/config --region <your-region>
```

#### 4. Install Dapr
```bash
helm repo add dapr https://daprio.github.io/helm-charts
helm repo update
helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait
```

#### 5. Deploy Application
```bash
helm install todo-app ./helm-charts/todo-app --values ./helm-charts/todo-app/values.yaml
```

#### 6. Configure Ingress
Update the ingress configuration with your domain:
```yaml
# In values.yaml
ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: todo-evolution.yourdomain.com  # Replace with your domain
      paths:
        - path: /
          pathType: Prefix
```

### CI/CD Pipeline

The GitHub Actions workflow automatically:
1. Runs tests on pull requests
2. Builds Docker images on main branch push
3. Pushes images to Oracle Container Registry
4. Deploys to Oracle Kubernetes Engine
5. Verifies deployment status

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@host:port/dbname
COHERE_API_KEY=your_cohere_api_key
JWT_SECRET=your_jwt_secret
BETTER_AUTH_SECRET=your_auth_secret
CORS_ORIGINS=https://yourdomain.com,http://localhost:3000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api
NEXT_PUBLIC_APP_URL=https://your-frontend-domain.com
```

## Security

### Authentication
- JWT-based authentication
- Role-based access control
- Secure secret management with OCI Vault

### Network Security
- Private cluster networking
- Network policies for pod isolation
- TLS encryption for all communications
- API rate limiting

## Monitoring and Observability

### Metrics Collection
- Application performance metrics
- Dapr sidecar metrics
- Kubernetes cluster metrics
- Database connection metrics

### Logging Strategy
- Structured JSON logging
- Centralized log aggregation
- Error tracking and alerting
- Audit trail for user actions

## Cost Management

### Free Tier Compliance
- Monitor resource utilization
- Stay within Oracle Cloud Always Free limits:
  - 4 ARM vCPUs
  - 24GB memory
  - 200GB storage
  - Monthly bandwidth allowance

### Resource Allocation
- ARM-based nodes for cost efficiency
- Resource limits and requests configured
- Optimized container images

## Success Criteria

- [x] App running on Oracle Cloud Kubernetes
- [x] All Phase 4 features working
- [x] Dapr installed and operational
- [x] Redpanda processing events
- [x] All 7 advanced features functional
- [x] CI/CD auto-deploying
- [x] Zero monthly cost
- [x] No credit card used

## Constraints

- Budget: $0/month forever
- No credit card anywhere
- Oracle Cloud Always Free only
- Self-hosted Redpanda (free)
- Open source Dapr (free)

## Oracle Cloud Always Free Includes

- 4 ARM CPU cores, 24GB RAM
- 200GB storage
- Kubernetes cluster
- Load balancer
- Container registry
- Network bandwidth

## Getting Started

1. Sign up for Oracle Cloud Always Free (email + phone only)
2. Set up your Kubernetes cluster
3. Configure the application with your domain
4. Deploy using Helm
5. Set up the CI/CD pipeline

## Troubleshooting

### Common Issues
- Resource limits exceeded: Check Oracle Cloud usage
- Connection timeouts: Verify network policies
- Image pull errors: Check container registry access
- Dapr sidecar issues: Verify Dapr installation

### Useful Commands
```bash
# Check pod status
kubectl get pods

# Check services
kubectl get svc

# Check logs
kubectl logs -f deployment/backend

# Check Dapr status
kubectl get pods -n dapr-system
```

## Demo

A live demo of the application is available at [your-domain.com](https://your-domain.com) (to be updated with actual deployment).