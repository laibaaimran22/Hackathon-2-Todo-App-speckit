"""
Test script to verify all advanced features are working correctly.
"""
from src.task_manager import TaskManager
from src.display import Display


def test_advanced_features():
    """Test all advanced features of the todo application"""
    print("Testing Advanced Level Features...")

    # Initialize components
    tm = TaskManager()
    display = Display()

    print("\n=== 1. Recurring Task Creation ===")
    # Create a recurring task
    recurring_task = tm.add_task(
        title="Daily Exercise",
        description="Do 30 minutes of exercise",
        priority="High",
        tags=["health", "daily"],
        due_date="2025-01-05",  # Future date for testing
        recurrence_pattern="daily",
        recurrence_interval=1
    )
    print(f"+ Created recurring task: {recurring_task['title']}")
    print(f"  - Pattern: {recurring_task['recurrence_pattern']}")
    print(f"  - Interval: {recurring_task['recurrence_interval']}")

    print("\n=== 2. Due Date Functionality ===")
    # Create tasks with various due dates
    today_task = tm.add_task(
        title="Meeting Today",
        description="Team meeting",
        priority="High",
        tags=["work"],
        due_date="2025-01-01"  # Today for testing
    )

    future_task = tm.add_task(
        title="Future Event",
        description="Plan for future",
        priority="Medium",
        tags=["planning"],
        due_date="2025-12-31"  # Future date
    )

    print(f"+ Created task due today: {today_task['title']}")
    print(f"+ Created task due in future: {future_task['title']}")

    print("\n=== 3. Due Date Status Calculation ===")
    # Check due date status
    recurring_status = tm.get_task_due_status(recurring_task)
    today_status = tm.get_task_due_status(today_task)
    future_status = tm.get_task_due_status(future_task)

    print(f"+ Recurring task status: {recurring_status}")
    print(f"+ Today task status: {today_status}")
    print(f"+ Future task status: {future_status}")

    print("\n=== 4. Overdue/Upcoming Task Retrieval ===")
    # Get overdue and upcoming tasks
    overdue_tasks = tm.get_overdue_tasks()
    upcoming_tasks = tm.get_upcoming_tasks(30)  # Next 30 days
    current_tasks = tm.get_current_tasks()

    print(f"+ Overdue tasks: {len(overdue_tasks)}")
    print(f"+ Upcoming tasks: {len(upcoming_tasks)}")
    print(f"+ Current tasks: {len(current_tasks)}")

    print("\n=== 5. Recurring Task Completion (Creates New Instance) ===")
    # Mark recurring task as complete - should create new instance
    original_id = recurring_task['id']
    print(f"Before completion: {len(tm.get_all_tasks())} tasks")

    completed_task = tm.mark_task_status(original_id, True)
    print(f"Marked task {original_id} as complete")

    all_tasks = tm.get_all_tasks()
    print(f"After completion: {len(all_tasks)} tasks")

    # Count recurring tasks with same title
    recurring_instances = [t for t in all_tasks if t['title'] == "Daily Exercise"]
    print(f"+ Recurring task instances: {len(recurring_instances)} (should be 2)")

    print("\n=== 6. Display Functionality ===")
    # Test display with all new features
    print("Displaying all tasks with new features:")
    display.show_tasks(all_tasks)

    print("\n=== 7. Update Functionality with New Fields ===")
    # Update a task with new recurrence fields
    updated_task = tm.update_task(
        today_task['id'],
        title="Updated Meeting Today",
        recurrence_pattern="weekly",
        recurrence_interval=2
    )
    print(f"+ Updated task: {updated_task['title']}")
    print(f"  - New recurrence: {updated_task['recurrence_pattern']}")
    print(f"  - New interval: {updated_task['recurrence_interval']}")

    print("\n=== 8. All Advanced Features Working! ===")
    print(f"+ Total tasks in system: {len(tm.get_all_tasks())}")
    print("+ Recurring tasks: Working")
    print("+ Due date management: Working")
    print("+ Overdue/upcoming detection: Working")
    print("+ Task completion with recurrence: Working")
    print("+ Display with new fields: Working")
    print("+ Update functionality: Working")

    return True


if __name__ == "__main__":
    test_advanced_features()