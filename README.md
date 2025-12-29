# Todo Application – Intermediate Level (Organization & Usability)

This is a console-based todo application that provides enhanced organization and usability features including task priorities, tags, search, filter, and sort functionality while maintaining all Phase 1 basic functionality.

## Features

### Phase 1 Features (Basic Functionality)
- Add new tasks with title and description
- View all tasks with clear status indicators
- Update existing task details
- Delete tasks by unique ID
- Mark tasks as complete or incomplete
- Console-based user interface
- In-memory storage (data lost on application exit)

### Phase 2 Features (Organization & Usability)
- **Task Priorities**: Assign priority levels (High, Medium, Low) to tasks
- **Tags / Categories**: Assign one or more tags to tasks for categorization
- **Search Tasks**: Search tasks by keyword in title or description
- **Filter Tasks**: Filter by completion status, priority level, or tags
- **Sort Tasks**: Sort by due date, priority, or alphabetically by title

## Requirements

- Python 3.13+
- UV for environment management

## Setup Instructions

1. Clone or download the repository
2. Navigate to the project directory
3. Install dependencies using UV:
   ```bash
   uv venv  # Create virtual environment
   uv pip install --system  # Install any required packages (none needed for this app)
   ```

## Run Instructions

To run the application:

```bash
python -m src.cli.todo_cli add "Task Title" --description "Task Description" --priority High --tags tag1 tag2 --due-date 2023-12-31
```

### List Tasks
```bash
python -m src.cli.todo_cli list
```

With filtering:
```bash
python -m src.cli.todo_cli list --status completed --priority High --tag work
```

With sorting:
```bash
python -m src.cli.todo_cli list --sort priority --reverse
```

### Search Tasks
```bash
python -m src.cli.todo_cli search "keyword"
```

### Mark Task as Complete
```bash
python -m src.cli.todo_cli complete 1
```

### Delete Task
```bash
python -m src.cli.todo_cli delete 1
```

## Architecture

The application follows a clean architecture with separation of concerns:

- `src/models/task.py`: Task model with extended functionality
- `src/services/task_service.py`: Business logic for task management
- `src/services/validation.py`: Validation functions for all new features
- `src/lib/utils.py`: Utility functions for sorting, filtering, and search
- `src/cli/todo_cli.py`: Command-line interface
- `tests/unit/`: Unit tests for models and services
- `tests/acceptance/`: Acceptance tests for all features

## Performance Goals

- Search/filter/sort operations complete in under 2 seconds
- Task creation with tags/priorities completes in under 5 seconds
- Display operations complete in under 200ms

## Technology Stack

- Python 3.13+
- Standard Python library only (no external dependencies)
- In-memory storage only
- Console-based interface

## Testing

Run unit tests:
```bash
python -m unittest discover -s tests/unit
```

Run acceptance tests:
```bash
python -m unittest discover -s tests/acceptance
```

## Backward Compatibility

All Phase 1 functionality remains unchanged and fully functional. The new features are additive and do not break existing behavior.