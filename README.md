# In-Memory Todo Console Application

A Phase I command-line todo application that stores tasks only in memory (no persistent storage). The application provides basic todo functionality including adding, viewing, updating, deleting, and marking tasks as complete/incomplete.

## Features

- Add new tasks with title and description
- View all tasks with clear status indicators
- Update existing task details
- Delete tasks by unique ID
- Mark tasks as complete or incomplete
- Console-based user interface
- In-memory storage (data lost on application exit)

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
python src/main.py
```

## Usage

The application provides a menu-driven interface:

1. **Add a new task**: Enter a title (required) and description (optional)
2. **View all tasks**: See all tasks with their IDs and completion status
3. **Update an existing task**: Modify title or description by task ID
4. **Delete a task**: Remove a task by its ID
5. **Mark task as complete/incomplete**: Update the completion status of a task
6. **Exit**: Quit the application

## Architecture

The application follows a simple layered architecture:
- `main.py`: Entry point and CLI interface
- `task_manager.py`: Core task operations and business logic
- `display.py`: Output formatting and display functions
- `models.py`: Task data model definition

## Project Structure

```
.
├── src/
│   ├── main.py          # Entry point and CLI interface
│   ├── task_manager.py  # Task operations and validation
│   ├── display.py       # Display formatting functions
│   └── models.py        # Task data model
├── specs/
│   └── 1-todo-app/
│       ├── spec.md      # Feature specification
│       ├── plan.md      # Implementation plan
│       └── checklists/
│           └── requirements.md  # Quality checklist
├── .specify/
│   └── memory/
│       └── constitution.md  # Project constitution
├── README.md
├── CLAUDE.md
└── CONSTITUTION.md
```

## Notes

- All data is stored in memory only and will be lost when the application terminates
- Task IDs are auto-generated as sequential numbers starting from 1
- The application follows clean Python practices with type hints