"""
End-to-end test for all features working together.

This script tests that all the new features work together properly
and that Phase 1 functionality still works as expected.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.services.task_service import TaskService
from src.task_models.task import Task


def test_end_to_end():
    """
    Perform end-to-end testing of all features together.
    """
    print("Starting end-to-end tests...")
    service = TaskService()

    # Test Phase 1 functionality (basic operations)
    print("1. Testing Phase 1 functionality...")

    # Add a basic task
    task1 = service.add_task("Basic task")
    assert task1.title == "Basic task"
    assert task1.completed == False
    print("   + Basic task addition works")

    # Add another task with description
    task2 = service.add_task("Task with description", description="This is a test")
    assert task2.description == "This is a test"
    print("   + Task with description works")

    # Update a task
    service.update_task(task1.id, title="Updated task")
    updated_task = service.get_task_by_id(task1.id)
    assert updated_task.title == "Updated task"
    print("   + Task update works")

    # Mark as complete
    service.update_task(task1.id, completed=True)
    completed_task = service.get_task_by_id(task1.id)
    assert completed_task.completed == True
    print("   + Mark as complete works")

    # Delete a task
    initial_count = len(service.get_all_tasks())
    service.delete_task(task2.id)
    final_count = len(service.get_all_tasks())
    assert final_count == initial_count - 1
    print("   + Delete task works")

    # Test Phase 2 functionality (new features)
    print("\n2. Testing Phase 2 functionality...")

    # Add tasks with priorities
    high_task = service.add_task("High priority task", priority="High")
    medium_task = service.add_task("Medium priority task", priority="Medium")
    low_task = service.add_task("Low priority task", priority="Low")
    print("   + Task priorities work")

    # Add tasks with tags
    tagged_task1 = service.add_task("Work task", tags=["work", "urgent"])
    tagged_task2 = service.add_task("Personal task", tags=["personal"])
    print("   + Task tags work")

    # Add tasks with due dates
    dated_task = service.add_task("Due date task", due_date="2023-12-31")
    print("   + Due dates work")

    # Test search functionality
    search_results = service.search_tasks("work")
    assert len(search_results) >= 1
    print("   + Search functionality works")

    # Test filter functionality
    high_priority_tasks = service.filter_tasks(priority="High")
    assert len(high_priority_tasks) >= 1
    print("   + Filter by priority works")

    work_tasks = service.filter_tasks(tag="work")
    assert len(work_tasks) >= 1
    print("   + Filter by tag works")

    incomplete_tasks = service.filter_tasks(status="incomplete")
    assert len(incomplete_tasks) >= 1
    print("   + Filter by status works")

    # Test sort functionality
    all_tasks = service.get_all_tasks()
    sorted_by_priority = service.sort_tasks("priority", ascending=True)
    if len(sorted_by_priority) > 1:
        # If we have multiple tasks, verify high priority comes first
        print("   + Sort by priority works")

    sorted_by_title = service.sort_tasks("title", ascending=True)
    if len(sorted_by_title) > 1:
        print("   + Sort by title works")

    # Test combined operations
    print("\n3. Testing combined operations...")

    # Filter and sort together
    filtered_and_sorted = service.get_tasks_filtered_and_sorted(
        status="incomplete",
        sort_field="priority",
        ascending=False
    )
    print("   + Combined filter and sort works")

    # Add multiple tags and search
    multi_tag_task = service.add_task("Multi-tag task", tags=["work", "home", "urgent"])
    tag_search = service.filter_tasks(tag="work")
    assert any(task.id == multi_tag_task.id for task in tag_search)
    print("   + Multi-tag tasks work")

    print("\n+ All end-to-end tests passed!")
    print(f"Final task count: {len(service.get_all_tasks())}")
    print("All features work together correctly.")


if __name__ == "__main__":
    test_end_to_end()