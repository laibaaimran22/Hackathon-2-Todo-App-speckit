# Data Model: Advanced Level Features

## Task Entity Extension

### Fields
- **id**: int - Unique identifier for the task (existing)
- **title**: str - Task title (existing)
- **description**: str - Task description (existing)
- **completed**: bool - Completion status (existing)
- **priority**: str - Priority level (High/Medium/Low) (existing from Intermediate)
- **tags**: List[str] - List of tags (existing from Intermediate)
- **due_date**: Optional[str] - Due date in YYYY-MM-DD format (new)
- **recurrence_pattern**: Optional[str] - Recurrence pattern (daily/weekly/monthly) (new)
- **recurrence_interval**: Optional[int] - Interval for recurrence (new, default: 1)

### Validation Rules
- **due_date**: Must be in YYYY-MM-DD format and represent a valid date
- **recurrence_pattern**: Must be one of "daily", "weekly", "monthly" or None
- **recurrence_interval**: Must be a positive integer when recurrence_pattern is set

### State Transitions
- **Task Creation**: New tasks can be created with or without due_date and recurrence_pattern
- **Task Completion**: When a recurring task is marked complete, a new instance is created with updated due_date
- **Due Date Status**: Task status can be "upcoming", "current", "overdue" based on due_date vs current date

## Recurrence Pattern Entity (Conceptual)

### Attributes
- **pattern_type**: str - The recurrence type (daily/weekly/monthly)
- **interval**: int - How often to repeat (e.g., every 2 weeks)
- **next_occurrence**: str - Calculated next occurrence date

## Due Date Entity (Conceptual)

### Attributes
- **date**: str - The due date in YYYY-MM-DD format
- **status**: str - "upcoming", "current", or "overdue" based on comparison with current date
- **days_until**: int - Number of days until due (negative if overdue)

## Backward Compatibility
- All new fields are optional to maintain compatibility with existing tasks
- Tasks without recurrence_pattern or due_date function exactly as before
- Existing data remains valid without modification