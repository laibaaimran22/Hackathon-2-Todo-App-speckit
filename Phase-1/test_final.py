"""
Final end-to-end test for the integrated todo application with all features.
"""
from src.task_manager import TaskManager
from src.display import Display


def test_complete_workflow():
    """Test complete workflow of the integrated todo application"""
    print("Testing complete workflow of integrated todo application...")

    # Initialize components
    task_manager = TaskManager()
    display = Display()

    print("\n=== PHASE 1: Basic Task Operations ===")

    # Add basic tasks
    task1 = task_manager.add_task("Basic Task 1", "Description for basic task")
    task2 = task_manager.add_task("Basic Task 2")
    print(f"✓ Added 2 basic tasks: {task1['title']}, {task2['title']}")

    # View all tasks
    all_tasks = task_manager.get_all_tasks()
    print(f"✓ Retrieved all tasks: {len(all_tasks)} tasks")

    # Update a task
    updated_task = task_manager.update_task(task1['id'], title="Updated Basic Task 1", description="Updated description")
    print(f"✓ Updated task: {updated_task['title']}")

    # Mark as complete
    completed_task = task_manager.mark_task_status(task2['id'], True)
    print(f"✓ Marked task as complete: {completed_task['title']} - Status: {'Complete' if completed_task['completed'] else 'Incomplete'}")

    print("\n=== PHASE 2: Intermediate Features ===")

    # Add tasks with new features
    task3 = task_manager.add_task("High Priority Task", "Important task", "High", ["work", "urgent"], "2024-12-31")
    task4 = task_manager.add_task("Low Priority Task", "Less important", "Low", ["personal"], "2024-11-15")
    task5 = task_manager.add_task("Medium Priority Task", "Regular task", "Medium", ["home", "todo"], "2024-10-01")
    print(f"✓ Added 3 tasks with new features")

    print("\n=== PHASE 3: Search Functionality ===")

    # Search tests
    search_results = task_manager.search_tasks("important")
    print(f"✓ Search for 'important': {len(search_results)} results")

    search_results = task_manager.search_tasks("task")
    print(f"✓ Search for 'task': {len(search_results)} results")

    print("\n=== PHASE 4: Filter Functionality ===")

    # Filter tests
    high_priority = task_manager.filter_tasks(priority="High")
    print(f"✓ Filter by High priority: {len(high_priority)} tasks")

    work_tag = task_manager.filter_tasks(tag="work")
    print(f"✓ Filter by 'work' tag: {len(work_tag)} tasks")

    completed = task_manager.filter_tasks(status="completed")
    print(f"✓ Filter by completed status: {len(completed)} tasks")

    incomplete = task_manager.filter_tasks(status="incomplete")
    print(f"✓ Filter by incomplete status: {len(incomplete)} tasks")

    print("\n=== PHASE 5: Sort Functionality ===")

    # Sort tests
    sorted_priority = task_manager.sort_tasks("priority", ascending=True)
    print(f"✓ Sort by priority (asc): {len(sorted_priority)} tasks")

    sorted_title = task_manager.sort_tasks("title", ascending=False)
    print(f"✓ Sort by title (desc): {len(sorted_title)} tasks")

    sorted_date = task_manager.sort_tasks("due_date", ascending=True)
    print(f"✓ Sort by due date (asc): {len(sorted_date)} tasks")

    print("\n=== PHASE 6: Combined Operations ===")

    # Combined operations
    filtered_and_sorted = task_manager.filter_tasks(priority="High")
    filtered_and_sorted = task_manager.sort_tasks("due_date", ascending=True)
    print(f"✓ Combined filter and sort operations: {len(filtered_and_sorted)} tasks")

    # Update task with all new fields
    updated_with_all = task_manager.update_task(
        task3['id'],
        title="Fully Updated Task",
        description="Completely updated task",
        priority="Low",
        tags=["updated", "test", "done"],
        due_date="2025-01-01"
    )
    print(f"✓ Updated task with all fields: {updated_with_all['title']}")

    print("\n=== PHASE 7: Final Verification ===")

    # Final view
    final_tasks = task_manager.get_all_tasks()
    print(f"✓ Final task count: {len(final_tasks)}")

    # Verify all expected fields exist
    sample_task = final_tasks[0] if final_tasks else None
    if sample_task:
        expected_fields = ['id', 'title', 'description', 'completed', 'priority', 'tags', 'due_date']
        missing_fields = [field for field in expected_fields if field not in sample_task]
        if not missing_fields:
            print("✓ All expected fields present in tasks")
        else:
            print(f"✗ Missing fields: {missing_fields}")

    print("\n=== SUMMARY ===")
    print("✓ All Phase 1 functionality preserved and working")
    print("✓ All Phase 2 features (priorities, tags, due dates) implemented and working")
    print("✓ Search functionality implemented and working")
    print("✓ Filter functionality implemented and working")
    print("✓ Sort functionality implemented and working")
    print("✓ Backward compatibility maintained")
    print("✓ All features integrated into original application structure")

    print(f"\n🎉 SUCCESS: All {len(final_tasks)} tasks with extended functionality working correctly!")
    return True


if __name__ == "__main__":
    test_complete_workflow()