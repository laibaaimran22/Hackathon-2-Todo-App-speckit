# Phase 5: Advanced Cloud Deployment Specification

## Overview
Deploy the Phase 4 todo application to Oracle Cloud Always Free tier with advanced features and event-driven architecture using Kubernetes, Dapr, and Redpanda. All components must operate within 100% free tier limits with zero monthly costs.

## Technology Stack (All Free)
- **Oracle Cloud Always Free**: Account with email + phone verification (no credit card)
- **Oracle Kubernetes Engine (OKE)**: Managed Kubernetes cluster
- **Dapr**: Open source microservices runtime
- **Redpanda Community**: Kafka-compatible event streaming platform
- **GitHub Actions**: CI/CD pipeline automation
- **Neon PostgreSQL**: Existing free tier database
- **Oracle Container Registry**: Free container image hosting

## Oracle Cloud Always Free Resources
- 4 ARM CPU cores, 24GB RAM (shared across all instances)
- 200GB storage
- 1 Kubernetes cluster
- Load balancer services
- Container registry with storage
- Network bandwidth allowances

## Advanced Features to Implement

### 1. Recurring Tasks
- Support daily, weekly, monthly recurring patterns
- Store recurrence rules in database
- Background job processor to create recurring tasks
- Handle recurrence exceptions and modifications

### 2. Due Dates with Email Reminders
- Task due date field with timezone support
- Email notification system (using SendGrid free tier or similar)
- Reminder scheduling before due dates
- Configurable reminder intervals (1 day, 1 hour, etc.)

### 3. Priority Levels
- High/Medium/Low priority classification
- Visual indicators for priority levels
- Priority-based sorting and filtering
- Priority escalation mechanisms

### 4. Tags/Categories
- User-defined tags for tasks
- Tag management interface
- Multi-tag assignment per task
- Tag-based filtering and grouping

### 5. Full-Text Search
- Search across task titles, descriptions, tags
- Real-time search suggestions
- Search result highlighting
- Boolean search operators support

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

## Event-Driven Architecture

### Event Types
- `task.created`: New task created
- `task.updated`: Task modified
- `task.completed`: Task marked as completed
- `task.reminder`: Due date reminder triggered
- `task.recurring`: Recurring task generation

### Architecture Components
- **Backend Services**: Publish events via Dapr
- **Redpanda Cluster**: Event streaming and persistence
- **Event Consumers**: Process tasks asynchronously
- **Dapr Sidecars**: Service-to-service communication
- **State Management**: Dapr state stores for task persistence

### Event Processing Flow
1. Frontend creates/modifies tasks via API
2. Backend publishes events to Redpanda via Dapr
3. Event consumers subscribe to relevant topics
4. Background processors handle business logic
5. State updates published back to Dapr state stores

## Deployment Architecture

### Infrastructure Components
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │────│   Load Balancer  │────│   Internet      │
│   (Next.js)     │    │   (OCI)          │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
┌─────────────────┐    ┌──────────────────┐
│   Backend       │────│   Dapr Sidecar   │
│   (FastAPI)     │    │   (Service Mesh) │
└─────────────────┘    └──────────────────┘
                              │
┌─────────────────┐    ┌──────────────────┐
│   Database      │    │   Redpanda       │
│   (Neon PG)     │    │   (Events)       │
└─────────────────┘    └──────────────────┘
```

### Kubernetes Manifests Required
- Deployment for Next.js frontend with Dapr sidecar
- Deployment for FastAPI backend with Dapr sidecar
- StatefulSet for Redpanda cluster
- Dapr components for pub/sub and state management
- Services for internal communication
- Ingress for external access

## CI/CD Pipeline (GitHub Actions)

### Build Stage
- Build Docker images for frontend and backend
- Scan images for vulnerabilities
- Push to Oracle Container Registry

### Test Stage
- Unit tests for all components
- Integration tests with Dapr mock
- Security scans

### Deploy Stage
- Apply Kubernetes manifests to OKE
- Rollout new versions with zero downtime
- Health checks and validation

### Trigger Events
- Push to main branch
- Pull request validation
- Manual deployment triggers

## Dapr Configuration

### Components to Configure
- **pubsub.redpanda**: Event publishing/subscribing
- **state.postgres**: State management with PostgreSQL
- **bindings.http**: HTTP endpoint bindings
- **middleware.http.bearer**: Authentication middleware

### Dapr Annotations for Pods
- Enable Dapr sidecar injection
- Configure app ports and protocols
- Set up secret management

## Redpanda Setup

### Topics to Create
- `task-events`: General task operations
- `reminders`: Due date notifications
- `recurring-tasks`: Recurring task processing
- `user-actions`: Audit logging

### Redpanda Configuration
- Single-node setup for free tier
- Data retention policies
- Topic partitioning strategy

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

## Security Considerations

### Network Security
- Private cluster networking
- Network policies for pod isolation
- TLS encryption for all communications
- API rate limiting

### Authentication & Authorization
- JWT-based authentication
- Role-based access control
- Secure secret management
- Input validation and sanitization

## Cost Optimization

### Free Tier Compliance
- Monitor resource utilization
- Auto-scaling within free limits
- Scheduled shutdown during low usage
- Efficient storage management

### Resource Allocation
- ARM-based nodes for cost efficiency
- Resource limits and requests configured
- Horizontal Pod Autoscaler disabled (fixed resources)
- Optimized container images

## Success Criteria

### Functional Requirements
- [ ] All Phase 4 features working in cloud environment
- [ ] All 7 advanced features implemented and functional
- [ ] Event-driven architecture operational
- [ ] Dapr services communicating properly
- [ ] Redpanda processing events reliably
- [ ] Full-text search working efficiently
- [ ] Advanced filtering and sorting operational

### Technical Requirements
- [ ] Application deployed on Oracle Kubernetes
- [ ] Dapr sidecars injected and operational
- [ ] Redpanda cluster running and accessible
- [ ] CI/CD pipeline automating deployments
- [ ] Zero monthly costs (within free tier)
- [ ] No credit card required anywhere
- [ ] 99% uptime SLA maintained

### Performance Requirements
- [ ] Response time < 500ms for API calls
- [ ] Page load time < 2 seconds
- [ ] Event processing latency < 1 second
- [ ] Database query time < 100ms

## Constraints and Limitations

### Oracle Cloud Free Tier Limits
- Maximum 4 ARM vCPUs
- Maximum 24GB memory
- Maximum 200GB storage
- Bandwidth limitations apply
- No GPU access

### Development Constraints
- No paid services allowed
- Credit card verification prohibited
- Self-hosted solutions only
- Open-source software required
- Community editions acceptable

## Risk Mitigation

### Technical Risks
- **Resource exhaustion**: Implement quotas and monitoring
- **Data loss**: Regular backups and replication
- **Service outages**: Health checks and failover mechanisms
- **Security breaches**: Regular security audits and updates

### Operational Risks
- **Vendor lock-in**: Use standard Kubernetes manifests
- **Scalability limits**: Plan for graceful degradation
- **Maintenance overhead**: Automated operations where possible
- **Knowledge transfer**: Comprehensive documentation

## Implementation Phases

### Phase 1: Infrastructure Setup
- Oracle Cloud account creation
- OKE cluster provisioning
- Dapr installation and configuration
- Redpanda deployment

### Phase 2: Application Migration
- Containerization of applications
- Dapr integration in services
- Event-driven architecture implementation
- Database migration planning

### Phase 3: Feature Enhancement
- Recurring tasks implementation
- Email reminder system
- Priority and tagging features
- Advanced search and filtering

### Phase 4: Deployment and Testing
- CI/CD pipeline setup
- End-to-end testing
- Performance optimization
- Documentation and handoff

## Acceptance Criteria

The Phase 5 deployment will be considered successful when:
1. Application is running on Oracle Cloud Kubernetes
2. All advanced features are functional and tested
3. Event-driven architecture is processing messages correctly
4. Monthly costs are $0 (within free tier)
5. No credit card was used during setup
6. CI/CD pipeline is operational
7. All security and performance requirements met