"""
Integration test for the updated todo application with all intermediate level features.
"""
from src.task_manager import TaskManager
from src.display import Display


def test_all_features():
    """Test all features of the updated todo application"""
    print("Testing all features of the updated todo application...")

    # Initialize components
    task_manager = TaskManager()
    display = Display()

    # Test 1: Add tasks with all new features
    print("\n1. Testing task creation with new features...")
    task1 = task_manager.add_task("Test Task 1", "This is a high priority task", "High", ["work", "urgent"], "2024-12-31")
    task2 = task_manager.add_task("Test Task 2", "This is a low priority task", "Low", ["personal"], "2024-11-15")
    task3 = task_manager.add_task("Another Task", "This has no tags", "Medium", [], "2024-10-01")

    print(f"Created {len(task_manager.get_all_tasks())} tasks")
    print(f"Task 1: {task1['title']} - Priority: {task1['priority']}, Tags: {task1['tags']}, Due: {task1['due_date']}")
    print(f"Task 2: {task2['title']} - Priority: {task2['priority']}, Tags: {task2['tags']}, Due: {task2['due_date']}")
    print(f"Task 3: {task3['title']} - Priority: {task3['priority']}, Tags: {task3['tags']}, Due: {task3['due_date']}")

    # Test 2: View all tasks
    print("\n2. Testing view all tasks...")
    all_tasks = task_manager.get_all_tasks()
    display.show_tasks(all_tasks)

    # Test 3: Search functionality
    print("\n3. Testing search functionality...")
    search_results = task_manager.search_tasks("high")
    print(f"Search for 'high' found {len(search_results)} tasks")
    for task in search_results:
        print(f"  - {task['title']}")

    search_results2 = task_manager.search_tasks("task")
    print(f"Search for 'task' found {len(search_results2)} tasks")
    for task in search_results2:
        print(f"  - {task['title']}")

    # Test 4: Filter functionality
    print("\n4. Testing filter functionality...")
    high_priority_tasks = task_manager.filter_tasks(priority="High")
    print(f"Filter by High priority: {len(high_priority_tasks)} tasks")
    for task in high_priority_tasks:
        print(f"  - {task['title']} (Priority: {task['priority']})")

    work_tag_tasks = task_manager.filter_tasks(tag="work")
    print(f"Filter by 'work' tag: {len(work_tag_tasks)} tasks")
    for task in work_tag_tasks:
        print(f"  - {task['title']} (Tags: {task['tags']})")

    incomplete_tasks = task_manager.filter_tasks(status="incomplete")
    print(f"Filter by incomplete status: {len(incomplete_tasks)} tasks")

    # Test 5: Sort functionality
    print("\n5. Testing sort functionality...")
    sorted_by_priority = task_manager.sort_tasks("priority", ascending=True)
    print("Sorted by priority (ascending):")
    for task in sorted_by_priority:
        print(f"  - {task['title']} (Priority: {task['priority']})")

    sorted_by_title = task_manager.sort_tasks("title", ascending=False)
    print("\nSorted by title (descending):")
    for task in sorted_by_title:
        print(f"  - {task['title']}")

    sorted_by_date = task_manager.sort_tasks("due_date", ascending=True)
    print("\nSorted by due date (ascending):")
    for task in sorted_by_date:
        print(f"  - {task['title']} (Due: {task['due_date']})")

    # Test 6: Update functionality with new fields
    print("\n6. Testing update functionality with new fields...")
    updated_task = task_manager.update_task(task1['id'], title="Updated Task 1", priority="Low", tags=["updated", "test"])
    print(f"Updated task: {updated_task['title']} - Priority: {updated_task['priority']}, Tags: {updated_task['tags']}")

    # Test 7: Mark as complete
    print("\n7. Testing mark as complete...")
    completed_task = task_manager.mark_task_status(task2['id'], True)
    print(f"Task {completed_task['id']} marked as {'complete' if completed_task['completed'] else 'incomplete'}")

    # Test 8: Final view to see all changes
    print("\n8. Final view of all tasks...")
    final_tasks = task_manager.get_all_tasks()
    display.show_tasks(final_tasks)

    print(f"\nAll tests completed successfully! Total tasks: {len(final_tasks)}")


if __name__ == "__main__":
    test_all_features()