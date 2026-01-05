# Implementation Plan: In-Memory Todo Console Application (Phase I – Basic Level)

## Architecture Overview

### System Architecture
The application will follow a simple layered architecture:
- **Presentation Layer**: CLI interface handling user input and displaying results
- **Business Logic Layer**: Task management operations and validation
- **Data Layer**: In-memory storage using Python dictionaries

### High-Level Design
```
┌─────────────────┐
│   CLI Layer     │ ← Command-line interface and user interaction
├─────────────────┤
│ Business Logic  │ ← Task operations (add, view, update, delete, mark status)
├─────────────────┤
│  Data Storage   │ ← In-memory dictionary storing tasks
└─────────────────┘
```

## Data Model

### Task Data Structure
- **Implementation**: Dictionary with numeric ID keys and task object values
- **Task Object Structure**:
  ```python
  {
    "id": int,           # Auto-incrementing numeric ID
    "title": str,        # Required task title
    "description": str,  # Optional task description
    "completed": bool    # Boolean status (True=Complete, False=Incomplete)
  }
  ```

### Memory Storage Design
- **Primary Storage**: `tasks: Dict[int, TaskObject]` - Dictionary keyed by task ID
- **ID Counter**: `next_id: int` - Auto-incrementing counter for generating unique IDs
- **Data Lifecycle**: All data exists only during application runtime

## Module Structure

### File Organization
```
src/
├── main.py                 # Entry point and CLI interface
├── task_manager.py         # Core task operations (add, update, delete, mark status)
├── display.py              # Output formatting and display functions
└── models.py               # Task data model and validation
```

### Module Responsibilities
1. **main.py**: Application entry point, main loop, menu handling, input processing
2. **task_manager.py**: Business logic for task operations, validation, and data manipulation
3. **display.py**: Functions for formatting and displaying tasks to users
4. **models.py**: Task data structure definition and validation utilities

## Implementation Details

### Task Management Functions
- `add_task(title: str, description: str = "")` → Task object with generated ID
- `get_all_tasks()` → List of all tasks sorted by ID
- `update_task(task_id: int, title: str = None, description: str = None)` → Updated task or None
- `delete_task(task_id: int)` → Boolean indicating success
- `mark_task_status(task_id: int, completed: bool)` → Updated task or None
- `get_task_by_id(task_id: int)` → Task object or None

### CLI Interaction Flow
1. **Main Menu**: Display operation options (Add, View, Update, Delete, Mark Status, Exit)
2. **Operation Selection**: Process user choice and call appropriate handler
3. **Input Collection**: Gather required parameters from user
4. **Operation Execution**: Call task management functions
5. **Result Display**: Show operation results or error messages
6. **Return to Menu**: Loop back to main menu unless user chooses to exit

### ID Generation Strategy
- **Implementation**: Auto-incrementing integer counter starting at 1
- **Management**: Maintain `next_id` variable that increments with each new task
- **Uniqueness**: Guarantee by design (increment-only counter)
- **Reset Behavior**: Counter resets to 1 when application starts (new session)

## Error Handling Strategy

### Input Validation
- **Required Fields**: Validate non-empty title for new tasks
- **Task ID Validation**: Verify task ID exists before update/delete/mark operations
- **Type Validation**: Ensure numeric inputs are properly converted

### Error Types and Responses
- **Invalid Task ID**: Display "Task not found" message when ID doesn't exist
- **Empty Title**: Display "Title is required" error when adding task without title
- **Invalid Menu Choice**: Display "Invalid option, please try again" for menu selection errors
- **General Errors**: Display user-friendly error messages without exposing internal details

## Implementation Sequence

### Phase 1: Core Data Layer (models.py, task_manager.py)
1. Define Task data model with validation
2. Implement task storage using in-memory dictionary
3. Create basic CRUD operations for tasks
4. Add ID generation and uniqueness logic

### Phase 2: Business Logic (task_manager.py)
1. Complete all task management functions
2. Add validation and error handling
3. Implement status management logic
4. Add data integrity checks

### Phase 3: Display Layer (display.py)
1. Create functions to format task display
2. Implement clear status indicators (✓/○)
3. Design consistent output formatting
4. Add empty state handling

### Phase 4: CLI Interface (main.py)
1. Build main application loop
2. Create menu system and navigation
3. Connect CLI to task management functions
4. Add error handling and user feedback

## Quality Assurance

### Testing Strategy
- **Unit Tests**: Test each function in isolation
- **Integration Tests**: Test CLI flow and end-to-end operations
- **Manual Acceptance**: Verify all 5 basic features meet specifications

### Acceptance Criteria by Feature
- **Add Task**: Successfully create tasks with title and optional description, with unique auto-generated IDs
- **View Tasks**: Display all tasks with IDs, titles, descriptions, and clear status indicators
- **Update Task**: Modify existing task's title/description while preserving ID and status
- **Delete Task**: Remove task by ID and confirm successful deletion
- **Mark Task Status**: Change task completion status while preserving other data

### Success Metrics
- All functional requirements from specification are implemented
- Performance: Operations complete within 1 second as specified
- User experience: Clear, intuitive menu-based interface
- Code quality: Follows clean Python practices with proper type hints

## Dependencies and Setup

### Python Requirements
- Python 3.13+ runtime
- Standard library only (no external dependencies)

### Project Structure
```
src/
├── main.py
├── task_manager.py
├── display.py
└── models.py
```

## Risk Mitigation

### Potential Issues
- **Memory Management**: For Phase I, with limited task count, memory usage is not a concern
- **ID Collision**: Auto-incrementing design prevents this issue
- **Data Loss**: Expected behavior (in-memory only) per specification

### Validation Points
- Each implemented feature directly maps to specification requirements
- All user scenarios from specification are supported
- Success criteria from specification are measurable and verifiable