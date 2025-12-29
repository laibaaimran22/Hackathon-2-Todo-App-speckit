"""
In-Memory Todo Console Application
Task management and business logic module with extended functionality
"""
from typing import Dict, List, Optional, Any
from models import Task
import re
import calendar
from datetime import datetime, timedelta


class TaskManager:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "", priority: str = "Medium",
                 tags: List[str] = None, due_date: str = None,
                 recurrence_pattern: str = None, recurrence_interval: int = 1) -> Task:
        """
        Add a new task with required title and optional description, priority, tags, due date, and recurrence
        Returns the created task with auto-generated ID
        """
        if not title:
            raise ValueError("Title is required")

        if tags is None:
            tags = []

        # Validate priority
        if priority not in ["High", "Medium", "Low"]:
            raise ValueError(f"Priority must be one of 'High', 'Medium', 'Low', got '{priority}'")

        # Validate tags
        for tag in tags:
            if not tag or not tag.strip():
                raise ValueError("Tag cannot be empty or contain only whitespace")

        # Validate due date
        if due_date is not None:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', due_date):
                raise ValueError(f"Due date must be in YYYY-MM-DD format, got '{due_date}'")

            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f"Invalid date: '{due_date}'")

        # Validate recurrence pattern
        if recurrence_pattern is not None:
            if recurrence_pattern not in ["daily", "weekly", "monthly"]:
                raise ValueError(f"Recurrence pattern must be one of 'daily', 'weekly', 'monthly', got '{recurrence_pattern}'")

        # Validate recurrence interval
        if recurrence_interval is not None and recurrence_interval <= 0:
            raise ValueError(f"Recurrence interval must be a positive integer, got '{recurrence_interval}'")

        task_id = self.next_id
        self.next_id += 1

        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "completed": False,  # New tasks start as incomplete
            "priority": priority,  # Default priority
            "tags": tags,  # List of tags
            "due_date": due_date,  # Optional due date
            "recurrence_pattern": recurrence_pattern,  # Optional recurrence pattern
            "recurrence_interval": recurrence_interval  # Recurrence interval (default: 1)
        }

        self.tasks[task_id] = task
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks sorted by ID"""
        return sorted(self.tasks.values(), key=lambda x: x["id"])

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a specific task by its ID"""
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None,
                    priority: str = None, tags: List[str] = None, due_date: str = None,
                    recurrence_pattern: str = None, recurrence_interval: int = None) -> Optional[Task]:
        """
        Update an existing task's title, description, priority, tags, due date, and/or recurrence
        Preserves task ID and completion status
        """
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]

        # Only update fields that are provided
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            task["title"] = title

        if description is not None:
            task["description"] = description

        if priority is not None:
            if priority not in ["High", "Medium", "Low"]:
                raise ValueError(f"Priority must be one of 'High', 'Medium', 'Low', got '{priority}'")
            task["priority"] = priority

        if tags is not None:
            for tag in tags:
                if not tag or not tag.strip():
                    raise ValueError("Tag cannot be empty or contain only whitespace")
            task["tags"] = tags

        if due_date is not None:
            if due_date is not None:
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', due_date):
                    raise ValueError(f"Due date must be in YYYY-MM-DD format, got '{due_date}'")

                try:
                    datetime.strptime(due_date, '%Y-%m-%d')
                except ValueError:
                    raise ValueError(f"Invalid date: '{due_date}'")
            task["due_date"] = due_date

        if recurrence_pattern is not None:
            if recurrence_pattern not in ["daily", "weekly", "monthly"]:
                raise ValueError(f"Recurrence pattern must be one of 'daily', 'weekly', 'monthly', got '{recurrence_pattern}'")
            task["recurrence_pattern"] = recurrence_pattern

        if recurrence_interval is not None:
            if recurrence_interval <= 0:
                raise ValueError(f"Recurrence interval must be a positive integer, got '{recurrence_interval}'")
            task["recurrence_interval"] = recurrence_interval

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def mark_task_status(self, task_id: int, completed: bool) -> Optional[Task]:
        """Mark a task as complete or incomplete. If the task is recurring and marked as complete, create a new instance."""
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        task["completed"] = completed

        # If the task is recurring and being marked as complete, create a new instance
        if completed and task.get("recurrence_pattern"):
            new_due_date = self._calculate_next_due_date(task)
            new_task = {
                "id": self.next_id,
                "title": task["title"],
                "description": task["description"],
                "completed": False,  # New instance starts as incomplete
                "priority": task["priority"],
                "tags": task["tags"],
                "due_date": new_due_date,
                "recurrence_pattern": task["recurrence_pattern"],
                "recurrence_interval": task["recurrence_interval"]
            }
            self.tasks[self.next_id] = new_task
            self.next_id += 1

        return task

    def _calculate_next_due_date(self, task: Task) -> Optional[str]:
        """Calculate the next due date based on the recurrence pattern."""
        if not task.get("due_date") or not task.get("recurrence_pattern"):
            return task.get("due_date")  # Return original due date if no recurrence

        try:
            current_date = datetime.strptime(task["due_date"], '%Y-%m-%d')
            pattern = task["recurrence_pattern"]
            interval = task.get("recurrence_interval", 1)

            if pattern == "daily":
                next_date = current_date + timedelta(days=interval)
            elif pattern == "weekly":
                next_date = current_date + timedelta(weeks=interval)
            elif pattern == "monthly":
                # Calculate next month (handle month overflow)
                year = current_date.year
                month = current_date.month + interval
                day = current_date.day

                # Adjust for month overflow
                while month > 12:
                    year += 1
                    month -= 12

                # Handle day overflow (e.g., Jan 31 + 1 month should be Feb 28/29)
                max_day = calendar.monthrange(year, month)[1]
                if day > max_day:
                    day = max_day

                next_date = datetime(year, month, day)
            else:
                return task["due_date"]  # Default to original if pattern is invalid

            return next_date.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            return task["due_date"]  # Return original if calculation fails

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title or description"""
        if not keyword or not keyword.strip():
            raise ValueError("Search keyword cannot be empty")

        keyword = keyword.strip().lower()
        matching_tasks = []

        for task in self.tasks.values():
            if (keyword in task["title"].lower() or
                keyword in task["description"].lower()):
                matching_tasks.append(task)

        return matching_tasks

    def get_task_due_status(self, task: Task) -> str:
        """Get the due status of a task: 'overdue', 'current', or 'upcoming'."""
        if not task.get("due_date"):
            return "no_due_date"

        try:
            due_date = datetime.strptime(task["due_date"], '%Y-%m-%d')
            current_date = datetime.now().date()
            due_date_only = due_date.date()

            if due_date_only < current_date:
                return "overdue"
            elif due_date_only == current_date:
                return "current"
            else:
                return "upcoming"
        except ValueError:
            return "invalid_due_date"

    def get_overdue_tasks(self) -> List[Task]:
        """Get all tasks that are overdue."""
        overdue_tasks = []
        for task in self.tasks.values():
            if self.get_task_due_status(task) == "overdue":
                overdue_tasks.append(task)
        return overdue_tasks

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks that are due within the specified number of days (default 7)."""
        upcoming_tasks = []
        current_date = datetime.now().date()

        for task in self.tasks.values():
            if task.get("due_date"):
                try:
                    due_date = datetime.strptime(task["due_date"], '%Y-%m-%d').date()
                    days_until_due = (due_date - current_date).days

                    if 0 <= days_until_due <= days:
                        upcoming_tasks.append(task)
                except ValueError:
                    continue  # Skip tasks with invalid due dates

        return upcoming_tasks

    def get_current_tasks(self) -> List[Task]:
        """Get tasks that are due today."""
        current_tasks = []
        for task in self.tasks.values():
            if self.get_task_due_status(task) == "current":
                current_tasks.append(task)
        return current_tasks

    def filter_tasks(self, status: str = None, priority: str = None, tag: str = None) -> List[Task]:
        """Filter tasks by status, priority, or tag"""
        filtered_tasks = list(self.tasks.values())

        if status is not None:
            if status == "completed":
                filtered_tasks = [task for task in filtered_tasks if task["completed"]]
            elif status == "incomplete":
                filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
            else:
                raise ValueError(f"Status must be one of 'completed', 'incomplete', got '{status}'")

        if priority is not None:
            if priority not in ["High", "Medium", "Low"]:
                raise ValueError(f"Priority must be one of 'High', 'Medium', 'Low', got '{priority}'")
            filtered_tasks = [task for task in filtered_tasks if task["priority"] == priority]

        if tag is not None:
            filtered_tasks = [task for task in filtered_tasks if tag in task["tags"]]

        return filtered_tasks

    def sort_tasks(self, sort_field: str, ascending: bool = True) -> List[Task]:
        """Sort tasks by the specified field"""
        if sort_field not in ["title", "priority", "due_date"]:
            raise ValueError(f"Sort field must be one of 'title', 'priority', 'due_date', got '{sort_field}'")

        def priority_order(priority: str) -> int:
            priority_map = {"High": 0, "Medium": 1, "Low": 2}
            return priority_map.get(priority, 1)  # Default to Medium if invalid

        if sort_field == "priority":
            return sorted(self.tasks.values(), key=lambda x: priority_order(x["priority"]), reverse=not ascending)
        elif sort_field == "due_date":
            def date_key(task: Task) -> Any:
                # Tasks without due dates get a high value to sort them to the end
                if task["due_date"] is None:
                    return (1, datetime.max) if ascending else (0, datetime.min)
                else:
                    # Convert date string to datetime for comparison
                    date_obj = datetime.strptime(task["due_date"], '%Y-%m-%d')
                    return (0, date_obj) if ascending else (1, date_obj)
            return sorted(self.tasks.values(), key=date_key)
        elif sort_field == "title":
            return sorted(self.tasks.values(), key=lambda x: x["title"].lower(), reverse=not ascending)
        else:
            return sorted(self.tasks.values(), key=lambda x: x["id"], reverse=not ascending)