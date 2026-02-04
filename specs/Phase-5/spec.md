# Phase 5: Advanced Cloud Deployment (100% Free)

## Overview
Deploy the Phase 4 todo application to Oracle Cloud Always Free tier with advanced features and event-driven architecture using Kubernetes, Dapr, and Redpanda. All components must operate within 100% free tier limits with zero monthly costs.

## Technology Stack (All Free)
- Oracle Cloud Always Free (email + phone verification, no credit card)
- Oracle Kubernetes Engine (OKE)
- Dapr (open source microservices runtime)
- Redpanda Community (Kafka-compatible event streaming)
- GitHub Actions (CI/CD pipeline)
- Neon PostgreSQL (existing free tier)

## Oracle Cloud Always Free Resources
- 4 ARM CPU cores, 24GB RAM
- 200GB storage
- Kubernetes cluster
- Load balancer services
- Container registry
- Network bandwidth allowances

## 7 Advanced Features to Implement

### 1. Recurring Tasks
- Support daily, weekly, monthly recurring patterns
- Background job processor for recurring tasks

### 2. Due dates with email reminders
- Task due date field with timezone support
- Email notification system for reminders

### 3. Priority levels (high/medium/low)
- Priority classification for tasks
- Priority-based sorting and filtering

### 4. Tags/categories
- User-defined tags for tasks
- Multi-tag assignment per task
- Tag-based filtering and grouping

### 5. Full-text search
- Search across task titles, descriptions, tags
- Real-time search suggestions

### 6. Advanced filters (by status/priority/tags/dates)
- Filter by status, priority, tags, dates
- Combined filter combinations

### 7. Sorting (by date/priority/name)
- Sort by creation date, due date, priority, name
- Custom sort orders

## Event-Driven Architecture
- Backend publishes events via Dapr
- Redpanda handles event streaming
- Event consumers process tasks asynchronously
- Topics: task.created, task.updated, task.completed, task.reminder

## Deployment Architecture
- Build Docker images for frontend/backend
- Push to Oracle Container Registry
- Deploy to OKE with Dapr sidecars
- CI/CD via GitHub Actions

## Dapr Configuration
- Pub/sub components with Redpanda
- State management with PostgreSQL
- Service-to-service communication
- Secret management

## Redpanda Setup
- Single-node cluster for free tier
- Task event topics
- Consumer groups for processing

## Success Criteria
- [ ] App running on Oracle Cloud Kubernetes
- [ ] All Phase 4 features working
- [ ] Dapr installed and operational
- [ ] Redpanda processing events
- [ ] All 7 features functional
- [ ] CI/CD auto-deploying
- [ ] Zero monthly cost
- [ ] No credit card used

## Constraints
- Budget: $0/month forever
- No credit card anywhere
- Oracle Cloud Always Free only
- Self-hosted Redpanda (free)
- Open source Dapr (free)