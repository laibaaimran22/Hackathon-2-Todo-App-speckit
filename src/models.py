"""
In-Memory Todo Console Application
Data models and validation module
"""
from typing import TypedDict


class Task(TypedDict):
    """
    Task data model
    Represents a single todo task with required fields and optional description
    """
    id: int
    title: str
    description: str
    completed: bool