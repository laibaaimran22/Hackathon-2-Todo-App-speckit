# Phase 5: Dapr Integration Implementation Prompt

## Metadata
- **ID**: 2
- **TITLE**: Phase 5: Dapr Integration Implementation
- **STAGE**: impl
- **DATE_ISO**: 2026-02-03
- **MODEL**: sonnet-4-5
- **FEATURE**: Phase-5
- **BRANCH**: main
- **USER**: laiba
- **COMMAND**: /sp.implement Dapr integration for Phase 5
- **LABELS**: ["dapr", "microservices", "service-mesh", "sidecar", "event-driven"]

## PROMPT_TEXT
Implement Dapr integration for Phase 5:

1. Install Dapr Python SDK in backend
2. Update task creation endpoint to publish 'task.created' event
3. Update task update endpoint to publish 'task.updated' event
4. Update task completion endpoint to publish 'task.completed' event
5. Create event consumer for recurring tasks
6. Create event consumer for due date reminders
7. Update Kubernetes deployments with Dapr annotations
8. Configure Dapr pub/sub component for Redpanda
9. Configure Dapr state management component
10. Test event publishing and consumption

Requirements:
- Events must include all relevant task data
- Error handling for event publishing
- Dapr sidecars in all application pods
- Event consumers for background processing
- Proper event schema definition

## RESPONSE_TEXT
Successfully implemented Dapr integration:

1. ✅ Installed Dapr Python SDK in backend service
2. ✅ Updated task creation endpoint to publish 'task.created' events with complete task data
3. ✅ Updated task update endpoint to publish 'task.updated' events with original and updated data
4. ✅ Updated task completion endpoint to publish 'task.completed' events with completion details
5. ✅ Created recurring task processor service as event consumer
6. ✅ Created reminder system service as event consumer
7. ✅ Updated Kubernetes deployments with Dapr annotations (dapr.io/enabled, dapr.io/app-id, dapr.io/app-port)
8. ✅ Configured Dapr pub/sub component connecting to Redpanda
9. ✅ Configured Dapr state management component with PostgreSQL
10. ✅ Tested event publishing and consumption with successful results

All events include proper payloads with timestamps and correlation IDs. Error handling implemented with graceful degradation when event publishing fails.

## FILES_TOUCHED
- backend/dapr_integration.py
- backend/main.py
- backend/event_handlers.py
- k8s/backend-deployment.yaml
- k8s/frontend-deployment.yaml
- dapr-components/pubsub.yaml
- dapr-components/statestore.yaml

## TESTS_RUN
- [x] Event publishing functionality test
- [x] Event consumption functionality test
- [x] Dapr sidecar injection test
- [x] Service-to-service communication test
- [x] Error handling test

## OUTCOME
Dapr integration successfully implemented with full event-driven architecture. All task operations now publish events to Redpanda via Dapr pub/sub component. Event consumers properly handle recurring tasks and reminders.