# Quickstart Guide: Advanced Level Features

## Implementation Overview

This guide covers the implementation of recurring tasks and time-based reminders for the console-based todo application.

## Key Components to Modify

### 1. models.py - Extend Task Model
- Add `due_date`, `recurrence_pattern`, and `recurrence_interval` fields to the Task TypedDict
- Maintain all existing fields for backward compatibility

### 2. task_manager.py - Add Business Logic
- Extend `add_task` method to accept recurrence and due date parameters
- Implement recurring task generation logic in `mark_task_status` method
- Add due date validation and status calculation methods
- Create methods to filter tasks by due date status (overdue, upcoming)

### 3. display.py - Update Display Logic
- Modify task display to show due dates and recurrence indicators
- Add visual indicators for overdue and upcoming tasks
- Update menu to include new options for due date and recurrence management

### 4. main.py - Extend CLI Interface
- Add new menu options for creating recurring tasks and managing due dates
- Implement input validation for new date and recurrence parameters
- Add functionality to view overdue and upcoming tasks

## Core Logic Implementation

### Recurring Task Generation
When a recurring task is marked as complete:
1. Calculate the next occurrence date based on the recurrence pattern
2. Create a new task with the same properties as the original
3. Set the new task's due date to the calculated next occurrence
4. Preserve the recurrence pattern for the new instance

### Due Date Management
- Store due dates in YYYY-MM-DD format
- Calculate task status (overdue/upcoming/current) based on comparison with current date
- Display appropriate visual indicators in the task list

## Testing Approach

### Manual Testing Steps
1. Create a recurring task with daily pattern
2. Mark the task as complete and verify a new instance is created
3. Create tasks with various due dates (past, present, future)
4. Verify overdue and upcoming tasks are properly identified
5. Confirm all existing functionality still works

### Validation Points
- All Basic and Intermediate features continue to work
- New features don't break existing task data
- Due date calculations are accurate
- Recurring tasks generate correctly without duplication