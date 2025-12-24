"""
In-Memory Todo Console Application
Task management and business logic module
"""
from typing import Dict, List, Optional
from models import Task


class TaskManager:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with required title and optional description
        Returns the created task with auto-generated ID
        """
        if not title:
            raise ValueError("Title is required")

        task_id = self.next_id
        self.next_id += 1

        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "completed": False  # New tasks start as incomplete
        }

        self.tasks[task_id] = task
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks sorted by ID"""
        return sorted(self.tasks.values(), key=lambda x: x["id"])

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a specific task by its ID"""
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description
        Preserves task ID and completion status
        """
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]

        # Only update fields that are provided
        if title is not None:
            task["title"] = title
        if description is not None:
            task["description"] = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def mark_task_status(self, task_id: int, completed: bool) -> Optional[Task]:
        """Mark a task as complete or incomplete"""
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        task["completed"] = completed
        return task