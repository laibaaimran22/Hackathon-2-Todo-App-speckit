# Quickstart Guide: Todo Application – Intermediate Level (Organization & Usability)

## Overview

This guide provides instructions for implementing the intermediate level todo application features including task priorities, tags, search, filter, and sort functionality.

## Implementation Steps

### 1. Extend Task Model
- Modify the existing Task class to include priority, tags, and due_date fields
- Add validation for new fields
- Set appropriate defaults for backward compatibility

### 2. Create Task Service
- Implement search functionality that searches in title and description
- Create filter functions for status, priority, and tags
- Implement sort functions for due_date, priority, and title
- Ensure all operations work on copies of data without modifying original

### 3. Update CLI Interface
- Extend add command with --priority and --tags options
- Add search command for keyword searching
- Add filter options to list command
- Add sort options to list command
- Ensure backward compatibility with existing commands

### 4. Add Validation Module
- Create validation functions for priority values
- Validate tag format and content
- Validate due date format
- Ensure error messages are user-friendly

### 5. Update Utility Functions
- Create sorting utility functions for different criteria
- Create filtering utility functions
- Add helper functions for display formatting

## Key Implementation Points

### Task Model Extension
```python
# Example of extended task structure
class Task:
    def __init__(self, id, title, description="", completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = "Medium"  # Default priority
        self.tags = []  # List of tags
        self.due_date = None  # Optional due date
```

### Priority Handling
- Store as string values: "High", "Medium", "Low"
- Implement comparison logic for sorting: High > Medium > Low
- Validate input against allowed values

### Tag Management
- Store as list of strings
- Validate for non-empty, trimmed content
- Support multiple tags per task

### Search Implementation
- Case-insensitive substring matching
- Search in both title and description fields
- Return original tasks (don't modify data)

### Filter Implementation
- Support filtering by completion status, priority, and tags
- Allow combination of multiple filters
- Return filtered view without modifying original data

### Sort Implementation
- Support sorting by due date, priority, and title
- Handle missing due dates appropriately (sort to end)
- Maintain priority ordering: High > Medium > Low