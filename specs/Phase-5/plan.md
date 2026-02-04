# Phase 5: Advanced Cloud Deployment Implementation Plan

## Overview
This plan outlines the implementation of Phase 5: deploying the todo application to Oracle Cloud Always Free tier with advanced features using Kubernetes, Dapr, and Redpanda. The application currently consists of a Next.js frontend and FastAPI backend with PostgreSQL database.

## Current Architecture
- **Frontend**: Next.js application (TypeScript)
- **Backend**: FastAPI application (Python 3.11)
- **Database**: PostgreSQL (via SqlModel/SQLAlchemy)
- **Authentication**: JWT-based custom implementation
- **Containerization**: Docker multi-stage builds
- **Orchestration**: Kubernetes deployments with Helm charts
- **AI Integration**: Cohere API integration with Model Context Protocol (MCP) tools

## Implementation Phases

### Phase 5.1: Oracle Cloud Setup
**Timeline**: Days 1-3
**Dependencies**: None

Tasks:
1. Create Oracle Cloud account using email and phone only (no credit card)
2. Set up compartment for the application
3. Create Virtual Cloud Network (VCN) with appropriate subnets
4. Deploy Oracle Kubernetes Engine (OKE) cluster
5. Configure OCI Object Storage for backups and assets
6. Set up Oracle Container Registry (OCIR)
7. Configure kubectl locally to connect to OKE cluster
8. Verify cluster connectivity and permissions

Deliverables:
- Active OKE cluster
- Configured OCIR
- Local kubectl configured
- Basic connectivity verified

### Phase 5.2: Dapr and Redpanda Installation
**Timeline**: Days 4-6
**Dependencies**: Phase 5.1 completed

Tasks:
1. Install Dapr control plane on OKE using Helm
2. Configure Dapr placement service for actor scaling
3. Deploy Redpanda cluster on OCI (self-hosted single node for free tier)
4. Configure Redpanda topics for application events
5. Set up Dapr components for pub/sub with Redpanda
6. Test basic event publishing/subscribing functionality
7. Configure Dapr state management with PostgreSQL
8. Set up Dapr secret management with OCI Vault

Deliverables:
- Dapr running on OKE
- Redpanda cluster operational
- Dapr components configured (pub/sub, state, secrets)
- Basic event streaming tested

### Phase 5.3: Add Advanced Features
**Timeline**: Days 7-14
**Dependencies**: Phase 5.1 and Phase 5.2 completed

Tasks:
1. Update database schema to support:
   - Priority levels (high/medium/low)
   - Due dates with timezone support
   - Tags/categories system
   - Recurrence patterns for tasks
   - Full-text search indexes
2. Backend modifications:
   - Add priority field to Task model
   - Add due_date field to Task model
   - Create Tag model and relationships
   - Implement recurrence logic
   - Add full-text search functionality
   - Update API endpoints to support new fields
3. Frontend modifications:
   - Add priority selection UI
   - Add due date picker
   - Create tag management interface
   - Implement recurrence pattern selection
   - Add search functionality
   - Update filtering and sorting UI
4. Test each feature locally before deployment

Deliverables:
- Updated database schema with new fields
- Backend API supporting all 7 features
- Frontend UI for all 7 features
- All features tested locally

### Phase 5.4: Event-Driven Architecture
**Timeline**: Days 15-18
**Dependencies**: Phase 5.3 completed

Tasks:
1. Integrate Dapr Python SDK into FastAPI backend
2. Implement event publishing to Redpanda for:
   - Task creation (`task.created`)
   - Task updates (`task.updated`)
   - Task completion (`task.completed`)
   - Due date reminders (`task.reminder`)
   - Recurring task generation (`task.recurring`)
3. Create event consumers for:
   - Email reminders service
   - Recurring task processor
   - Audit logging
4. Implement Dapr service invocation for internal communication
5. Set up event-driven notifications
6. Test complete event flow from creation to processing

Deliverables:
- Backend publishing events to Redpanda via Dapr
- Event consumers processing tasks
- Complete event-driven workflow tested

### Phase 5.5: Deploy to Oracle Cloud
**Timeline**: Days 19-21
**Dependencies**: Phases 5.1, 5.2, 5.3, and 5.4 completed

Tasks:
1. Update Docker images to include Dapr integration
2. Build new Docker images for frontend and backend with Dapr sidecars
3. Push images to Oracle Container Registry
4. Update Kubernetes manifests with Dapr annotations:
   - Enable Dapr sidecar injection
   - Configure app-id and app-port
   - Set up service invocation endpoints
5. Deploy updated application to OKE
6. Configure load balancer and ingress for external access
7. Set up HTTPS with Oracle's certificate management
8. Verify all services are running and accessible

Deliverables:
- Application deployed to OKE with Dapr sidecars
- External access via load balancer
- HTTPS enabled
- All services operational

### Phase 5.6: CI/CD Pipeline
**Timeline**: Days 22-24
**Dependencies**: Phase 5.5 completed

Tasks:
1. Create GitHub Actions workflow for CI/CD:
   - Build Docker images on code changes
   - Run unit and integration tests
   - Scan images for vulnerabilities
   - Push images to OCIR
   - Deploy to OKE with rolling updates
2. Set up automated testing before deployment
3. Configure deployment triggers (on merge to main branch)
4. Implement rollback procedures
5. Test CI/CD pipeline with a sample change
6. Set up notifications for deployment status

Deliverables:
- Automated CI/CD pipeline operational
- Automated testing integrated
- Deployment notifications configured

### Phase 5.7: Testing and Documentation
**Timeline**: Days 25-28
**Dependencies**: All previous phases completed

Tasks:
1. Comprehensive testing:
   - All Phase 4 features still working
   - All 7 new features functional
   - Event-driven flows working correctly
   - Performance under load
   - Security validation
2. Update documentation:
   - README with deployment instructions
   - Architecture diagram
   - API documentation
   - Troubleshooting guide
3. Create demo recording showing all features
4. Performance optimization based on testing results
5. Security hardening measures

Deliverables:
- All features tested and functional
- Complete documentation
- Demo recording
- Optimized and secured application

## Success Criteria
- [ ] App running on Oracle Cloud Kubernetes
- [ ] All Phase 4 features working
- [ ] Dapr installed and operational
- [ ] Redpanda processing events
- [ ] All 7 features functional:
  - Recurring tasks (daily/weekly/monthly)
  - Due dates with email reminders
  - Priority levels (high/medium/low)
  - Tags/categories
  - Full-text search
  - Advanced filters (by status/priority/tags/dates)
  - Sorting (by date/priority/name)
- [ ] CI/CD auto-deploying
- [ ] Zero monthly cost
- [ ] No credit card used

## Risk Mitigation
- Resource constraints: Monitor usage within free tier limits
- Complexity: Implement features incrementally with thorough testing
- Dependencies: Use only free-tier compatible services
- Security: Implement proper authentication and authorization

## Critical Files to Modify
- `Phase-5/backend/app/models/task.py` - Update Task model with new fields
- `Phase-5/backend/app/api/tasks.py` - Update API endpoints with new functionality
- `Phase-5/frontend/src/components/Tasks/TaskList.jsx` - Update UI for new features
- `Phase-5/k8s/deployment.yaml` - Add Dapr annotations and configurations
- `Phase-5/helm/values.yaml` - Update Helm chart values for Dapr
- `Phase-5/.github/workflows/deploy.yml` - CI/CD pipeline configuration

## Verification Steps
1. Deploy the application to OKE
2. Verify all 7 advanced features are working
3. Confirm events are flowing through Redpanda via Dapr
4. Test the CI/CD pipeline with a code change
5. Validate that all costs remain within free tier limits
6. Perform security and performance testing