# API Contracts: Advanced Level Features

## Task Creation with Advanced Features

### Endpoint: `TaskManager.add_task(title, description, priority, tags, due_date, recurrence_pattern, recurrence_interval)`

**Request Parameters**:
- `title`: str (required) - Task title
- `description`: str (optional) - Task description
- `priority`: str (optional, default: "Medium") - Priority level (High/Medium/Low)
- `tags`: List[str] (optional, default: []) - List of tags
- `due_date`: Optional[str] (optional) - Due date in YYYY-MM-DD format
- `recurrence_pattern`: Optional[str] (optional) - Recurrence pattern (daily/weekly/monthly)
- `recurrence_interval`: Optional[int] (optional) - Recurrence interval

**Response**: Task object with all fields including the new advanced fields

**Validation**:
- Due date must be in YYYY-MM-DD format
- Recurrence pattern must be one of: daily, weekly, monthly
- Recurrence interval must be a positive integer when recurrence is set

## Task Completion with Recurrence

### Endpoint: `TaskManager.mark_task_status(task_id, completed)`

**Request Parameters**:
- `task_id`: int - Task identifier
- `completed`: bool - Completion status

**Response**: Updated Task object

**Behavior**:
- If task is recurring and marked as complete, creates a new instance with updated due date
- Original task maintains completion status
- New instance has new task ID and updated due date based on recurrence pattern

## Due Date Status Methods

### Endpoint: `TaskManager.get_overdue_tasks()`

**Response**: List of tasks with due dates in the past

### Endpoint: `TaskManager.get_upcoming_tasks()`

**Response**: List of tasks with due dates in the future

### Endpoint: `TaskManager.get_current_tasks()`

**Response**: List of tasks with due dates today