# Data Model: Todo Application – Intermediate Level (Organization & Usability)

## Entity: Task

**Description**: Represents a todo item with title, description, completion status, priority level, tags, and optional due date

**Fields**:
- `id` (int): Auto-generated unique identifier for the task
- `title` (str): Title of the task (inherited from Phase 1)
- `description` (str): Detailed description of the task (inherited from Phase 1)
- `completed` (bool): Completion status of the task (inherited from Phase 1)
- `priority` (str): Priority level - one of "High", "Medium", "Low" with "Medium" as default
- `tags` (list[str]): List of user-defined tags for categorization, default is empty list
- `due_date` (str or None): Optional due date in YYYY-MM-DD format

**Validation Rules**:
- `priority` must be one of: "High", "Medium", "Low" (case-sensitive)
- `tags` must be a list of non-empty, trimmed strings
- `due_date` must follow YYYY-MM-DD format if provided
- `title` and `description` follow existing Phase 1 validation rules

**State Transitions**:
- Creation: New task with default priority "Medium", empty tags list
- Update: Priority and tags can be modified; completion status toggled
- Completion: `completed` changes from False to True

## Entity: Priority

**Description**: An enumeration with values High, Medium, Low that indicates the importance of a task

**Values**:
- "High": Highest priority tasks requiring immediate attention
- "Medium": Standard priority tasks (default)
- "Low": Lowest priority tasks that can be deferred

**Ordering**: High > Medium > Low for sorting operations

## Entity: Tag

**Description**: A user-defined text label that can be associated with one or more tasks for categorization

**Constraints**:
- Must be a non-empty string after trimming whitespace
- Cannot be just whitespace
- Multiple tags per task allowed
- Case-sensitive (e.g., "Work" and "work" are different tags)

## Entity: SearchQuery

**Description**: Represents a search query for finding tasks by keyword

**Fields**:
- `keyword` (str): The search term to match against title and description
- `case_sensitive` (bool): Whether search should be case-sensitive (default: False)

## Entity: FilterCriteria

**Description**: Represents criteria for filtering tasks

**Fields**:
- `status` (str or None): Filter by completion status ("completed", "incomplete", None for all)
- `priority` (str or None): Filter by priority level ("High", "Medium", "Low", None for all)
- `tag` (str or None): Filter by specific tag (None for all)
- `completed` (bool or None): Direct completion status filter (None for all)

## Entity: SortCriteria

**Description**: Represents criteria for sorting tasks

**Fields**:
- `by` (str): Field to sort by ("due_date", "priority", "title")
- `ascending` (bool): Sort direction (True for ascending, False for descending)

**Special Handling**:
- Tasks without due dates sort to the end when sorting by due_date
- Priority sorting follows High > Medium > Low order
- Title sorting is alphabetical