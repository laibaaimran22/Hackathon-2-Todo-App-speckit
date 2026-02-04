# Phase 5: Advanced Cloud Deployment - Task Specification

## Overview
Detailed breakdown of implementation tasks for Phase 5: Advanced Cloud Deployment with event-driven architecture using Oracle Cloud, Dapr, and Redpanda.

## Task Breakdown

### Task 1: Oracle Cloud Infrastructure Setup
**Objective**: Set up Oracle Cloud Always Free infrastructure
**Time Estimate**: 3 days

#### Subtasks:
- [x] Create Oracle Cloud account with email + phone (no credit card)
- [x] Create compartment for the application
- [x] Set up Virtual Cloud Network (VCN) with subnets
- [x] Deploy Oracle Kubernetes Engine (OKE) cluster
- [x] Configure OCI Object Storage
- [x] Set up Oracle Container Registry (OCIR)
- [x] Configure kubectl locally for OKE access
- [x] Verify cluster connectivity and permissions

#### Acceptance Criteria:
- [x] OKE cluster running and accessible
- [x] OCIR configured and accessible
- [x] kubectl connected to cluster
- [x] Basic kubectl commands work (get nodes, get pods)

### Task 2: Dapr and Redpanda Installation
**Objective**: Install and configure Dapr and Redpanda on OKE
**Time Estimate**: 2 days

#### Subtasks:
- [x] Install Dapr control plane on OKE using Helm
- [x] Configure Dapr placement service
- [x] Deploy Redpanda cluster (single node for free tier)
- [x] Configure Redpanda topics for application events
- [x] Set up Dapr pub/sub component for Redpanda
- [x] Set up Dapr state store component with PostgreSQL
- [x] Set up Dapr secret store component with OCI Vault
- [x] Test basic event publishing/subscribing

#### Acceptance Criteria:
- [x] Dapr control plane running in dapr-system namespace
- [x] Redpanda cluster operational
- [x] Dapr components configured and healthy
- [x] Test event published and consumed successfully

### Task 3: Backend - Priority Levels Implementation
**Objective**: Add priority levels to task management system
**Time Estimate**: 1 day

#### Subtasks:
- [x] Update Task model with priority field (high/medium/low)
- [x] Add priority validation in model
- [x] Update TaskCreate schema to accept priority
- [x] Update TaskUpdate schema to accept priority
- [x] Update TaskRead schema to include priority
- [x] Add priority to task creation endpoint
- [x] Add priority to task update endpoint
- [x] Add priority filtering to get tasks endpoint
- [x] Update database migrations for priority column

#### Acceptance Criteria:
- [x] Task model includes priority field
- [x] API accepts priority during task creation/update
- [x] Priority values are validated (high/medium/low)
- [x] Tasks can be filtered by priority
- [x] Database schema updated with priority column

### Task 4: Backend - Due Dates Implementation
**Objective**: Add due date functionality with timezone support
**Time Estimate**: 1 day

#### Subtasks:
- [x] Update Task model with due_date field
- [x] Add timezone support to due_date
- [x] Update TaskCreate schema to accept due_date
- [x] Update TaskUpdate schema to accept due_date
- [x] Update TaskRead schema to include due_date
- [x] Add due_date to task creation endpoint
- [x] Add due_date to task update endpoint
- [x] Add due date filtering to get tasks endpoint
- [x] Add due date range filtering (start/end dates)
- [x] Update database migrations for due_date column

#### Acceptance Criteria:
- [x] Task model includes due_date field with timezone
- [x] API accepts due_date during task creation/update
- [x] Tasks can be filtered by due date
- [x] Date range filtering works correctly
- [x] Database schema updated with due_date column

### Task 5: Backend - Tags/Categories Implementation
**Objective**: Add tags/categories system for task organization
**Time Estimate**: 2 days

#### Subtasks:
- [x] Create Tag model with user relationship
- [x] Create TaskTagLink model for many-to-many relationship
- [x] Update Task model to include tags relationship
- [x] Create tag creation endpoint
- [x] Create tag retrieval endpoint
- [x] Update task creation to accept tag_names
- [x] Update task update to accept tag_names
- [x] Add tag filtering to get tasks endpoint
- [x] Implement tag assignment/removal logic
- [x] Update database migrations for Tag and TaskTagLink tables

#### Acceptance Criteria:
- [x] Tag model created with proper relationships
- [x] Task model includes tags relationship
- [x] API supports tag assignment during task operations
- [x] Tasks can be filtered by tags
- [x] Tags can be retrieved for a user
- [x] Database schema updated with Tag and TaskTagLink tables

### Task 6: Backend - Recurring Tasks Implementation
**Objective**: Add recurring task functionality
**Time Estimate**: 1 day

#### Subtasks:
- [x] Update Task model with recurrence_pattern field
- [x] Add recurrence validation (daily/weekly/monthly)
- [x] Update TaskCreate schema to accept recurrence_pattern
- [x] Update TaskUpdate schema to accept recurrence_pattern
- [x] Update TaskRead schema to include recurrence_pattern
- [x] Add recurrence_pattern to task creation endpoint
- [x] Add recurrence_pattern to task update endpoint
- [x] Create endpoint to get recurring tasks
- [x] Implement recurrence pattern validation
- [x] Update database migrations for recurrence_pattern column

#### Acceptance Criteria:
- [x] Task model includes recurrence_pattern field
- [x] API accepts recurrence patterns during task creation/update
- [x] Recurrence patterns are validated (daily/weekly/monthly)
- [x] Recurring tasks can be retrieved separately
- [x] Database schema updated with recurrence_pattern column

### Task 7: Backend - Full-Text Search Implementation
**Objective**: Add full-text search across task fields
**Time Estimate**: 1 day

#### Subtasks:
- [x] Add full-text search indexes to database
- [x] Create search endpoint with query parameter
- [x] Implement search across title, description, and tags
- [x] Add search result ranking/sorting
- [x] Implement search result highlighting (if feasible)
- [x] Test search performance with large datasets
- [x] Update database migrations for search indexes

#### Acceptance Criteria:
- [x] Search endpoint available and functional
- [x] Search works across title, description, and tags
- [x] Search results are ranked appropriately
- [x] Database includes full-text search indexes
- [x] Search performs well with reasonable dataset sizes

### Task 8: Backend - Advanced Filters Implementation
**Objective**: Add comprehensive filtering capabilities
**Time Estimate**: 1 day

#### Subtasks:
- [x] Add status filter (completed/pending/all)
- [x] Add priority filter (high/medium/low/all)
- [x] Add tag filter (specific tags or all)
- [x] Add date range filter (due date range)
- [x] Add combination filter support
- [x] Update get tasks endpoint with filter parameters
- [x] Optimize database queries for filtering
- [x] Add filter validation and error handling

#### Acceptance Criteria:
- [x] All filter types work independently
- [x] Multiple filters can be combined
- [x] Filtered results are returned correctly
- [x] Invalid filter values return appropriate errors
- [x] Filter queries are optimized for performance

### Task 9: Backend - Sorting Options Implementation
**Objective**: Add multiple sorting capabilities
**Time Estimate**: 1 day

#### Subtasks:
- [x] Add sort by creation date (ascending/descending)
- [x] Add sort by due date (ascending/descending)
- [x] Add sort by priority (high to low, low to high)
- [x] Add sort by title (alphabetical)
- [x] Add multi-field sorting support
- [x] Update get tasks endpoint with sort parameters
- [x] Implement sort validation and error handling
- [x] Test sorting performance with large datasets

#### Acceptance Criteria:
- [x] All sorting options work correctly
- [x] Sort direction (asc/desc) works properly
- [x] Multiple field sorting works
- [x] Invalid sort parameters return appropriate errors
- [x] Sorting performs well with reasonable dataset sizes

### Task 10: Frontend - Priority UI Implementation
**Objective**: Add priority level visualization and selection
**Time Estimate**: 1 day

#### Subtasks:
- [x] Update Task model type to include priority
- [x] Add priority dropdown to task creation form
- [x] Add priority dropdown to task edit modal
- [x] Add priority visual indicators to task list
- [x] Add priority color coding system
- [x] Add priority filtering controls to UI
- [x] Update task display to show priority level
- [x] Test priority UI functionality

#### Acceptance Criteria:
- [x] Priority can be selected during task creation
- [x] Priority can be edited in task edit modal
- [x] Priority levels are visually represented in task list
- [x] Priority filtering controls are available in UI
- [x] Priority changes are persisted to backend

### Task 11: Frontend - Due Date UI Implementation
**Objective**: Add due date selection and display
**Time Estimate**: 1 day

#### Subtasks:
- [x] Update Task model type to include due_date
- [x] Add date/time picker to task creation form
- [x] Add date/time picker to task edit modal
- [x] Add due date display to task list items
- [x] Add overdue task visual indicators
- [x] Add due date filtering controls to UI
- [x] Add date range filtering UI
- [x] Test due date UI functionality

#### Acceptance Criteria:
- [x] Due date can be selected during task creation
- [x] Due date can be edited in task edit modal
- [x] Due dates are displayed in task list items
- [x] Overdue tasks are visually indicated
- [x] Due date filtering controls work correctly
- [x] Due date changes are persisted to backend

### Task 12: Frontend - Tags UI Implementation
**Objective**: Add tag management interface
**Time Estimate**: 1 day

#### Subtasks:
- [x] Update Task model type to include tags
- [x] Add tag input to task creation form
- [x] Add tag input to task edit modal
- [x] Add tag display to task list items
- [x] Add tag filtering controls to UI
- [x] Add tag management page (optional)
- [x] Add tag autocomplete functionality
- [x] Test tag UI functionality

#### Acceptance Criteria:
- [x] Tags can be added during task creation
- [x] Tags can be modified in task edit modal
- [x] Tags are displayed in task list items
- [x] Tag filtering controls work correctly
- [x] Tag changes are persisted to backend

### Task 13: Frontend - Recurring Tasks UI Implementation
**Objective**: Add recurring task configuration UI
**Time Estimate**: 1 day

#### Subtasks:
- [x] Update Task model type to include recurrence_pattern
- [x] Add recurrence pattern selector to task creation form
- [x] Add recurrence pattern selector to task edit modal
- [x] Add recurring task indicator to task list
- [x] Add recurring tasks filter to UI
- [x] Test recurring task UI functionality

#### Acceptance Criteria:
- [x] Recurrence patterns can be selected during task creation
- [x] Recurrence patterns can be edited in task edit modal
- [x] Recurring tasks are visually indicated in task list
- [x] Recurring task filtering works correctly
- [x] Recurrence pattern changes are persisted to backend

### Task 14: Frontend - Search UI Implementation
**Objective**: Add full-text search interface
**Time Estimate**: 1 day

#### Subtasks:
- [x] Add search input field to task list page
- [x] Implement search debouncing/throttling
- [x] Add search results highlighting (if feasible)
- [x] Add search result count display
- [x] Implement search keyboard shortcuts (optional)
- [x] Add search history/clear functionality
- [x] Test search UI performance

#### Acceptance Criteria:
- [x] Search input field is available and functional
- [x] Search results update in real-time or with reasonable delay
- [x] Search results are displayed properly
- [x] Search performance is acceptable
- [x] Search functionality connects to backend search API

### Task 15: Frontend - Advanced Filters UI Implementation
**Objective**: Add comprehensive filter controls to UI
**Time Estimate**: 1 day

#### Subtasks:
- [x] Add status filter controls (completed/pending/all)
- [x] Add priority filter controls (high/medium/low/all)
- [x] Add tag filter controls (dropdown or chips)
- [x] Add date range filter controls
- [x] Add filter combination interface
- [x] Add filter reset functionality
- [x] Add active filter indicators
- [x] Test advanced filter UI functionality

#### Acceptance Criteria:
- [x] All filter types are available in UI
- [x] Multiple filters can be applied simultaneously
- [x] Filtered results update in real-time
- [x] Active filters are clearly indicated
- [x] Filter reset functionality works correctly

### Task 16: Frontend - Sorting UI Implementation
**Objective**: Add sorting controls to UI
**Time Estimate**: 1 day

#### Subtasks:
- [x] Add sort by dropdown (creation date, due date, priority, title)
- [x] Add sort direction controls (ascending/descending)
- [x] Add active sort indicator
- [x] Add multi-field sort controls (optional)
- [x] Implement sort persistence across page reloads
- [x] Test sorting UI functionality

#### Acceptance Criteria:
- [x] Sort by options are available in UI
- [x] Sort direction can be toggled
- [x] Active sort is clearly indicated
- [x] Sorting changes are applied to task list
- [x] Sort settings persist across page reloads

### Task 17: Dapr Event Integration - Task Creation Events
**Objective**: Publish events when tasks are created
**Time Estimate**: 1 day

#### Subtasks:
- [x] Install Dapr Python SDK in backend
- [x] Update task creation endpoint to publish 'task.created' event
- [x] Format event payload with task data
- [x] Add error handling for event publishing
- [x] Test event publishing functionality
- [x] Verify event appears in Redpanda

#### Acceptance Criteria:
- [x] Dapr SDK integrated into backend
- [x] 'task.created' events published when tasks are created
- [x] Event payload contains all relevant task data
- [x] Event publishing errors are handled gracefully
- [x] Events appear correctly in Redpanda

### Task 18: Dapr Event Integration - Task Update Events
**Objective**: Publish events when tasks are updated
**Time Estimate**: 1 day

#### Subtasks:
- [x] Update task update endpoint to publish 'task.updated' event
- [x] Format event payload with original and updated task data
- [x] Add field change tracking to event payload
- [x] Add error handling for event publishing
- [x] Test event publishing functionality
- [x] Verify event appears in Redpanda

#### Acceptance Criteria:
- [x] 'task.updated' events published when tasks are updated
- [x] Event payload contains original and updated data
- [x] Field changes are tracked in event payload
- [x] Event publishing errors are handled gracefully
- [x] Events appear correctly in Redpanda

### Task 19: Dapr Event Integration - Task Completion Events
**Objective**: Publish events when tasks are completed
**Time Estimate**: 1 day

#### Subtasks:
- [x] Update task completion endpoint to publish 'task.completed' event
- [x] Format event payload with completion details
- [x] Add completion timestamp to event
- [x] Add error handling for event publishing
- [x] Test event publishing functionality
- [x] Verify event appears in Redpanda

#### Acceptance Criteria:
- [x] 'task.completed' events published when tasks are completed
- [x] Event payload contains completion details
- [x] Completion timestamp is included in event
- [x] Event publishing errors are handled gracefully
- [x] Events appear correctly in Redpanda

### Task 20: Event Consumer - Recurring Task Processor
**Objective**: Create consumer for generating recurring tasks
**Time Estimate**: 1 day

#### Subtasks:
- [x] Create recurring task processor service
- [x] Subscribe to 'task.created' events
- [x] Check for recurrence patterns in events
- [x] Generate next occurrence based on pattern
- [x] Create new task for next occurrence
- [x] Handle recurrence termination conditions
- [x] Test recurring task generation

#### Acceptance Criteria:
- [x] Recurring task processor service running
- [x] Service subscribes to 'task.created' events
- [x] Recurring tasks are generated based on patterns
- [x] Next occurrences are created correctly
- [x] Recurrence termination is handled properly

### Task 21: Event Consumer - Reminder System
**Objective**: Create consumer for sending due date reminders
**Time Estimate**: 1 day

#### Subtasks:
- [x] Create reminder processor service
- [x] Subscribe to task events with due dates
- [x] Schedule reminders before due dates
- [x] Implement reminder delivery mechanism
- [x] Handle reminder cancellation for completed tasks
- [x] Test reminder functionality
- [x] Add reminder configuration options

#### Acceptance Criteria:
- [x] Reminder processor service running
- [x] Service subscribes to relevant task events
- [x] Reminders are scheduled and sent appropriately
- [x] Reminders are cancelled for completed tasks
- [x] Reminder system is configurable

### Task 22: Kubernetes Deployment - Dapr Annotations
**Objective**: Update Kubernetes deployments with Dapr sidecar annotations
**Time Estimate**: 0.5 days

#### Subtasks:
- [x] Add Dapr annotations to backend deployment
- [x] Add Dapr annotations to frontend deployment
- [x] Configure Dapr app-id and app-port
- [x] Configure Dapr config reference
- [x] Test Dapr sidecar injection
- [x] Verify Dapr components are accessible

#### Acceptance Criteria:
- [x] Dapr sidecars injected into all application pods
- [x] Dapr annotations configured correctly
- [x] Application services can communicate via Dapr
- [x] Dapr health checks pass

### Task 23: CI/CD Pipeline - GitHub Actions Workflow
**Objective**: Create automated CI/CD pipeline
**Time Estimate**: 1 day

#### Subtasks:
- [x] Create GitHub Actions workflow file
- [x] Set up build stage for Docker images
- [x] Add test stage for unit/integration tests
- [x] Add security scanning stage
- [x] Create deploy stage to OKE
- [x] Add verification stage for deployment
- [x] Configure branch protection rules
- [x] Test CI/CD pipeline functionality

#### Acceptance Criteria:
- [x] GitHub Actions workflow created and functional
- [x] Build stage creates Docker images
- [x] Test stage runs unit/integration tests
- [x] Security scanning passes
- [x] Deploy stage updates OKE deployment
- [x] Verification stage confirms deployment success
- [x] Branch protection enforces CI/CD requirements

### Task 24: Documentation and Testing
**Objective**: Complete documentation and testing
**Time Estimate**: 1 day

#### Subtasks:
- [x] Write deployment documentation
- [x] Create architecture diagrams
- [x] Write API documentation
- [x] Create user guides
- [x] Write troubleshooting guides
- [x] Create comprehensive test suite
- [x] Perform end-to-end testing
- [x] Document cost optimization strategies

#### Acceptance Criteria:
- [x] Deployment documentation complete and accurate
- [x] Architecture diagrams created and explained
- [x] API documentation covers all endpoints
- [x] User guides explain all features
- [x] Troubleshooting guides cover common issues
- [x] Test suite covers all functionality
- [x] End-to-end testing passes successfully

## Overall Acceptance Criteria
- [x] All 7 advanced features implemented (recurring tasks, due dates, priority levels, tags, full-text search, advanced filters, sorting)
- [x] Event-driven architecture operational with Dapr and Redpanda
- [x] Application deployed to Oracle Cloud Kubernetes
- [x] CI/CD pipeline operational
- [x] Zero monthly cost maintained
- [x] No credit card used anywhere
- [x] All functionality tested and working
- [x] Complete documentation provided