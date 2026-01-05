# API Contracts: Todo Application – Intermediate Level

## Task Creation with Priority and Tags

### Endpoint: `add_task(title, description="", priority="Medium", tags=[], due_date=None)`

**Input**:
- `title` (string, required): Task title
- `description` (string, optional): Task description, default empty string
- `priority` (string, optional): Priority level ("High", "Medium", "Low"), default "Medium"
- `tags` (array[string], optional): List of tags, default empty array
- `due_date` (string, optional): Due date in YYYY-MM-DD format

**Output**: Task object with all fields

**Validation**:
- Priority must be one of "High", "Medium", "Low"
- Tags must be non-empty strings after trimming
- Due date must follow YYYY-MM-DD format if provided

## Task Search

### Endpoint: `search_tasks(keyword)`

**Input**:
- `keyword` (string, required): Search term to match in title or description

**Output**: Array of Task objects matching the keyword

**Behavior**:
- Case-insensitive substring matching
- Matches in either title or description
- Returns original tasks without modification

## Task Filter

### Endpoint: `filter_tasks(criteria)`

**Input**:
- `criteria` (object): Filter criteria with optional fields:
  - `status` (string): "completed", "incomplete", or null for all
  - `priority` (string): "High", "Medium", "Low", or null for all
  - `tag` (string): Specific tag to filter by, or null for all

**Output**: Array of Task objects matching all criteria

**Behavior**:
- Applies all specified criteria as AND conditions
- Returns original tasks without modification

## Task Sort

### Endpoint: `sort_tasks(tasks, sort_criteria)`

**Input**:
- `tasks` (array): Array of Task objects to sort
- `sort_criteria` (object): Sorting criteria:
  - `by` (string): Field to sort by ("due_date", "priority", "title")
  - `ascending` (boolean): Sort direction

**Output**: Array of Task objects sorted according to criteria

**Behavior**:
- Sorts by due_date: tasks without due_date appear last
- Sorts by priority: High > Medium > Low
- Sorts by title: alphabetical
- Returns sorted copy without modifying original tasks