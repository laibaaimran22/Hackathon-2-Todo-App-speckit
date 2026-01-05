"""
Validation module for the todo application.

This module provides validation functions for all new features
including priorities, tags, search, filter, and sort functionality.
"""

from typing import List, Optional, Union
from datetime import datetime


def validate_priority(priority: str) -> bool:
    """
    Validate that the priority is one of the allowed values.

    Args:
        priority: Priority level to validate

    Returns:
        True if priority is valid, False otherwise

    Allowed values: "High", "Medium", "Low"
    """
    return priority in ["High", "Medium", "Low"]


def validate_tag(tag: str) -> bool:
    """
    Validate that the tag is not empty or just whitespace.

    Args:
        tag: Tag to validate

    Returns:
        True if tag is valid, False otherwise
    """
    if not tag or not tag.strip():
        return False
    return True


def validate_tags(tags: List[str]) -> bool:
    """
    Validate that all tags in the list are valid.

    Args:
        tags: List of tags to validate

    Returns:
        True if all tags are valid, False otherwise
    """
    return all(validate_tag(tag) for tag in tags)


def validate_due_date(due_date: Optional[str]) -> bool:
    """
    Validate that the due date is in the correct format (YYYY-MM-DD) and is a real date.

    Args:
        due_date: Due date to validate or None

    Returns:
        True if due date is valid or None, False otherwise
    """
    if due_date is None:
        return True

    # Check format YYYY-MM-DD
    if not isinstance(due_date, str) or len(due_date) != 10:
        return False

    if not due_date[0:4].isdigit() or due_date[4] != '-' or not due_date[5:7].isdigit() or due_date[7] != '-' or not due_date[8:10].isdigit():
        return False

    try:
        datetime.strptime(due_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_multiple_values(values: List[str], allowed_values: List[str]) -> bool:
    """
    Validate that all values in the list are in the allowed values.

    Args:
        values: List of values to validate
        allowed_values: List of allowed values

    Returns:
        True if all values are allowed, False otherwise
    """
    return all(value in allowed_values for value in values)


def validate_search_keyword(keyword: str) -> bool:
    """
    Validate that the search keyword is not empty.

    Args:
        keyword: Search keyword to validate

    Returns:
        True if keyword is valid, False otherwise
    """
    return bool(keyword and keyword.strip())


def validate_sort_field(field: str) -> bool:
    """
    Validate that the sort field is one of the allowed values.

    Args:
        field: Sort field to validate

    Returns:
        True if field is valid, False otherwise

    Allowed values: "due_date", "priority", "title"
    """
    return field in ["due_date", "priority", "title"]


def validate_filter_status(status: Optional[str]) -> bool:
    """
    Validate that the filter status is one of the allowed values.

    Args:
        status: Filter status to validate or None

    Returns:
        True if status is valid or None, False otherwise

    Allowed values: "completed", "incomplete", None
    """
    if status is None:
        return True
    return status in ["completed", "incomplete"]


def validate_filter_priority(priority: Optional[str]) -> bool:
    """
    Validate that the filter priority is one of the allowed values.

    Args:
        priority: Filter priority to validate or None

    Returns:
        True if priority is valid or None, False otherwise

    Allowed values: "High", "Medium", "Low", None
    """
    if priority is None:
        return True
    return priority in ["High", "Medium", "Low"]


def validate_filter_tag(tag: Optional[str]) -> bool:
    """
    Validate that the filter tag is valid.

    Args:
        tag: Filter tag to validate or None

    Returns:
        True if tag is valid or None, False otherwise
    """
    if tag is None:
        return True
    return validate_tag(tag)


def sanitize_tag(tag: str) -> str:
    """
    Sanitize a tag by stripping whitespace.

    Args:
        tag: Tag to sanitize

    Returns:
        Sanitized tag
    """
    return tag.strip()


def sanitize_tags(tags: List[str]) -> List[str]:
    """
    Sanitize a list of tags by stripping whitespace from each.

    Args:
        tags: List of tags to sanitize

    Returns:
        List of sanitized tags
    """
    return [sanitize_tag(tag) for tag in tags if validate_tag(tag)]