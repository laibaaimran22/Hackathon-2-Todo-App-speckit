"""
In-Memory Todo Console Application
Data models and validation module with extended functionality
"""
from typing import TypedDict, List, Optional
import re
from datetime import datetime


class Task(TypedDict):
    """
    Task data model
    Represents a single todo task with required fields and optional description
    Extended with priority, tags, due date, and recurrence for advanced level functionality
    """
    id: int
    title: str
    description: str
    completed: bool
    priority: str  # "High", "Medium", "Low"
    tags: List[str]  # List of tags
    due_date: Optional[str]  # Due date in YYYY-MM-DD format
    recurrence_pattern: Optional[str]  # Recurrence pattern: daily, weekly, monthly
    recurrence_interval: Optional[int]  # Recurrence interval (default: 1)