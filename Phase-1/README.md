# Phase 1: In-Memory Python Console Todo App

## Overview
A command-line todo application with in-memory storage implementing 5 basic features. This implementation also includes some intermediate features like priorities and tags that were added during this phase.

## Features
1. **Add Task** - Create new todo items with title, description, priority, and tags.
2. **Delete Task** - Remove tasks from life by unique ID.
3. **Update Task** - Modify task details including title and description.
4. **View Task List** - Display all tasks with options to filter and sort.
5. **Mark as Complete** - Toggle completion status.

## Technology Stack
- **Language:** Python 3.13+
- **Package Manager:** UV

## Setup Instructions
1. Install [UV](https://github.com/astral-sh/uv).
2. Create virtual environment:
   ```bash
   uv venv
   ```

## Running the Application
To see all commands:
```bash
python -m src.cli.todo_cli --help
```

Example (Add Task):
```bash
python -m src.cli.todo_cli add "Buy Milk" --description "Get 2L semi-skimmed"
```

## Running Tests
Run unit tests:
```bash
python -m unittest discover -s tests/unit
```

## Completion Status
✅ All Phase 1 features implemented and tested.
