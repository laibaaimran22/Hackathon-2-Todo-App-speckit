# Phase 1 Requirements: CLI Todo Application

## 1. Feature Requirements

### FR1: Add Task
- **User Story**: As a user, I want to create a new task so that I can track what I need to do.
- **Acceptance Criteria**:
  - Must accept a title (required) and a description (optional).
  - Should allow setting a priority (High, Medium, Low).
  - Should allow adding multiple tags.
  - Generates a unique ID for each task.

### FR2: Delete Task
- **User Story**: As a user, I want to remove a task from my list so that I can keep it clean.
- **Acceptance Criteria**:
  - Must accept a task ID.
  - Should provide feedback if the ID doesn't exist.

### FR3: Update Task
- **User Story**: As a user, I want to modify my tasks if details change.
- **Acceptance Criteria**:
  - Must allow updating title or description of an existing task ID.

### FR4: View Task List
- **User Story**: As a user, I want to see all my tasks in an organized list.
- **Acceptance Criteria**:
  - Should display ID, Status, Priority, Tags, and Title.
  - Should support filtering by status (completed/pending), priority, or tags.
  - Should support sorting by priority or title.

### FR5: Mark as Complete
- **User Story**: As a user, I want to mark tasks as done so I can track my progress.
- **Acceptance Criteria**:
  - Toggle completion status of a task by ID.

## 2. Non-Functional Requirements
- **Performance**: Listing and searching tasks should feel instantaneous (under 200ms).
- **Usability**: CLI commands should be intuitive with clear help text.
- **Storage**: In-memory storage for this phase (no persistence required).

## 3. Edge Cases Handled
- Adding a task with empty title (Blocked).
- Deleting or Updating a non-existent task ID (Handled with error message).
- Filtering by a tag that no tasks have (Empty list returned).
