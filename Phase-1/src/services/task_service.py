"""
Task service for the todo application.

This module provides business logic for task management including
search, filter, and sort functionality.
"""

from typing import List, Optional, Dict, Any
from src.task_models.task import Task
from src.lib import utils
from src.services import validation


class TaskService:
    """
    Service class for managing tasks with extended functionality.
    """

    def __init__(self):
        """
        Initialize the TaskService.
        """
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, title: str, description: str = "", priority: str = "Medium",
                 tags: List[str] = None, due_date: Optional[str] = None,
                 completed: bool = False) -> Task:
        """
        Add a new task with the specified parameters.

        Args:
            title: Task title
            description: Task description (default: "")
            priority: Task priority ("High", "Medium", "Low") (default: "Medium")
            tags: List of tags for the task (default: [])
            due_date: Due date in YYYY-MM-DD format (default: None)
            completed: Completion status (default: False)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If any of the parameters are invalid
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate priority
        if not validation.validate_priority(priority):
            raise ValueError(f"Priority must be one of 'High', 'Medium', 'Low', got '{priority}'")

        # Validate tags
        if tags is None:
            tags = []
        if not validation.validate_tags(tags):
            raise ValueError("One or more tags are invalid (empty or whitespace only)")

        # Validate due date
        if not validation.validate_due_date(due_date):
            raise ValueError(f"Due date must be in YYYY-MM-DD format, got '{due_date}'")

        # Create the task
        task = Task(self.next_id, title, description)
        task.set_priority(priority)
        task.set_due_date(due_date)
        task.completed = completed  # Set completion status

        # Add tags
        for tag in tags:
            task.add_tag(tag)

        self.tasks.append(task)
        self.next_id += 1

        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks
        """
        return self.tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str = None, description: str = None,
                    completed: bool = None, priority: str = None, tags: List[str] = None,
                    due_date: Optional[str] = None) -> bool:
        """
        Update a task with the specified parameters.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
            priority: New priority (optional)
            tags: New tags (optional)
            due_date: New due date (optional)

        Returns:
            True if task was updated, False if task was not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description

        if completed is not None:
            task.completed = completed

        if priority is not None:
            if not validation.validate_priority(priority):
                raise ValueError(f"Priority must be one of 'High', 'Medium', 'Low', got '{priority}'")
            task.set_priority(priority)

        if tags is not None:
            if not validation.validate_tags(tags):
                raise ValueError("One or more tags are invalid (empty or whitespace only)")
            task.tags = tags.copy()

        if due_date is not None:
            if not validation.validate_due_date(due_date):
                raise ValueError(f"Due date must be in YYYY-MM-DD format, got '{due_date}'")
            task.set_due_date(due_date)

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if task was not found
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title and description.

        Args:
            keyword: Keyword to search for

        Returns:
            List of tasks containing the keyword in title or description
        """
        if not validation.validate_search_keyword(keyword):
            raise ValueError("Search keyword cannot be empty")

        return utils.search_tasks(self.tasks, keyword)

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[str] = None,
                     tag: Optional[str] = None) -> List[Task]:
        """
        Filter tasks by various criteria.

        Args:
            status: Filter by completion status ("completed", "incomplete", None for all)
            priority: Filter by priority ("High", "Medium", "Low", None for all)
            tag: Filter by tag (None for all)

        Returns:
            List of tasks matching all specified criteria
        """
        # Validate inputs
        if status is not None and not validation.validate_filter_status(status):
            raise ValueError(f"Status must be one of 'completed', 'incomplete', got '{status}'")

        if priority is not None and not validation.validate_filter_priority(priority):
            raise ValueError(f"Priority must be one of 'High', 'Medium', 'Low', got '{priority}'")

        if tag is not None and not validation.validate_filter_tag(tag):
            raise ValueError(f"Tag cannot be empty or contain only whitespace, got '{tag}'")

        # Start with all tasks
        filtered_tasks = self.tasks.copy()

        # Apply filters sequentially
        filtered_tasks = utils.filter_by_status(filtered_tasks, status)
        filtered_tasks = utils.filter_by_priority(filtered_tasks, priority)
        filtered_tasks = utils.filter_by_tag(filtered_tasks, tag)

        return filtered_tasks

    def sort_tasks(self, sort_field: str, ascending: bool = True) -> List[Task]:
        """
        Sort tasks by the specified field.

        Args:
            sort_field: Field to sort by ("due_date", "priority", "title")
            ascending: Sort order (True for ascending, False for descending)

        Returns:
            List of tasks sorted by the specified field
        """
        if not validation.validate_sort_field(sort_field):
            raise ValueError(f"Sort field must be one of 'due_date', 'priority', 'title', got '{sort_field}'")

        return utils.sort_tasks(self.tasks, sort_field, ascending)

    def get_tasks_sorted(self, sort_field: str, ascending: bool = True) -> List[Task]:
        """
        Get tasks sorted by the specified field.

        Args:
            sort_field: Field to sort by ("due_date", "priority", "title")
            ascending: Sort order (True for ascending, False for descending)

        Returns:
            List of tasks sorted by the specified field
        """
        return self.sort_tasks(sort_field, ascending)

    def get_tasks_filtered_and_sorted(self, status: Optional[str] = None,
                                      priority: Optional[str] = None,
                                      tag: Optional[str] = None,
                                      sort_field: Optional[str] = None,
                                      ascending: bool = True) -> List[Task]:
        """
        Get tasks filtered by criteria and optionally sorted.

        Args:
            status: Filter by completion status ("completed", "incomplete", None for all)
            priority: Filter by priority ("High", "Medium", "Low", None for all)
            tag: Filter by tag (None for all)
            sort_field: Field to sort by ("due_date", "priority", "title", None for no sort)
            ascending: Sort order (True for ascending, False for descending)

        Returns:
            List of tasks matching criteria, optionally sorted
        """
        # First apply filters
        filtered_tasks = self.filter_tasks(status, priority, tag)

        # Then apply sorting if requested
        if sort_field is not None:
            return utils.sort_tasks(filtered_tasks, sort_field, ascending)

        return filtered_tasks