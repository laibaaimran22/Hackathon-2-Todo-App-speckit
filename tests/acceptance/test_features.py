"""
Acceptance tests for the todo application features.

This module tests all the new features: priorities, tags, search, filter, and sort.
"""

import unittest
import sys
from io import StringIO
from unittest.mock import patch
from src.services.task_service import TaskService
from src.cli.todo_cli import TodoCLI


class TestUserStory1_Priorities(unittest.TestCase):
    """
    Acceptance tests for User Story 1: Assign Task Priorities
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.service = TaskService()

    def test_create_task_with_priority(self):
        """
        Test creating a task with a specific priority level.
        """
        task = self.service.add_task("Test task", priority="High")

        self.assertEqual(task.priority, "High")
        self.assertEqual(len(self.service.get_all_tasks()), 1)

    def test_task_with_default_priority(self):
        """
        Test that tasks have default priority when none is specified.
        """
        task = self.service.add_task("Test task")

        self.assertEqual(task.priority, "Medium")
        self.assertEqual(len(self.service.get_all_tasks()), 1)

    def test_view_task_with_priority(self):
        """
        Test that priority information is displayed when viewing tasks.
        """
        task = self.service.add_task("Test task", priority="Low")
        all_tasks = self.service.get_all_tasks()

        self.assertEqual(len(all_tasks), 1)
        self.assertEqual(all_tasks[0].priority, "Low")


class TestUserStory2_Tags(unittest.TestCase):
    """
    Acceptance tests for User Story 2: Tag Tasks with Categories
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.service = TaskService()

    def test_create_task_with_tags(self):
        """
        Test creating a task with one or more tags.
        """
        task = self.service.add_task("Test task", tags=["work", "urgent"])

        self.assertIn("work", task.tags)
        self.assertIn("urgent", task.tags)
        self.assertEqual(len(task.tags), 2)

    def test_view_task_with_tags(self):
        """
        Test that tags are displayed when viewing tasks.
        """
        task = self.service.add_task("Test task", tags=["personal"])
        all_tasks = self.service.get_all_tasks()

        self.assertEqual(len(all_tasks), 1)
        self.assertIn("personal", all_tasks[0].tags)


class TestUserStory3_Search(unittest.TestCase):
    """
    Acceptance tests for User Story 3: Search Tasks by Keyword
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.service = TaskService()
        self.service.add_task("Complete project", "Finish the todo app project", priority="High")
        self.service.add_task("Buy groceries", "Milk, eggs, bread", priority="Medium")
        self.service.add_task("Call doctor", "Schedule appointment", priority="Low")

    def test_search_by_title(self):
        """
        Test searching for tasks by keyword in title.
        """
        results = self.service.search_tasks("project")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Complete project")

    def test_search_by_description(self):
        """
        Test searching for tasks by keyword in description.
        """
        results = self.service.search_tasks("milk")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Buy groceries")

    def test_search_case_insensitive(self):
        """
        Test that search is case-insensitive.
        """
        results = self.service.search_tasks("PROJECT")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Complete project")


class TestUserStory4_Filter(unittest.TestCase):
    """
    Acceptance tests for User Story 4: Filter Tasks by Criteria
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.service = TaskService()
        self.service.add_task("High priority task", priority="High")
        self.service.add_task("Medium priority task", priority="Medium")
        self.service.add_task("Low priority task", priority="Low", completed=True)
        self.service.add_task("Work task", tags=["work"])
        self.service.add_task("Personal task", tags=["personal"])

    def test_filter_by_status(self):
        """
        Test filtering tasks by completion status.
        """
        incomplete_tasks = self.service.filter_tasks(status="incomplete")
        completed_tasks = self.service.filter_tasks(status="completed")

        self.assertEqual(len(incomplete_tasks), 4)  # 4 incomplete tasks
        self.assertEqual(len(completed_tasks), 1)   # 1 completed task

    def test_filter_by_priority(self):
        """
        Test filtering tasks by priority level.
        """
        high_priority_tasks = self.service.filter_tasks(priority="High")
        medium_priority_tasks = self.service.filter_tasks(priority="Medium")
        low_priority_tasks = self.service.filter_tasks(priority="Low")

        self.assertEqual(len(high_priority_tasks), 1)
        self.assertEqual(len(medium_priority_tasks), 3)  # Includes 1 explicit + 2 defaults
        self.assertEqual(len(low_priority_tasks), 1)

    def test_filter_by_tag(self):
        """
        Test filtering tasks by tag.
        """
        work_tasks = self.service.filter_tasks(tag="work")
        personal_tasks = self.service.filter_tasks(tag="personal")

        self.assertEqual(len(work_tasks), 1)
        self.assertEqual(len(personal_tasks), 1)


class TestUserStory5_Sort(unittest.TestCase):
    """
    Acceptance tests for User Story 5: Sort Tasks by Different Criteria
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.service = TaskService()
        self.service.add_task("Zebra task", priority="Low", due_date="2023-12-31")
        self.service.add_task("Alpha task", priority="High", due_date="2023-01-01")
        self.service.add_task("Middle task", priority="Medium", due_date="2023-06-15")

    def test_sort_by_priority(self):
        """
        Test sorting tasks by priority level.
        """
        sorted_tasks = self.service.sort_tasks("priority", ascending=True)

        # High priority should come first
        self.assertEqual(sorted_tasks[0].priority, "High")
        self.assertEqual(sorted_tasks[-1].priority, "Low")

    def test_sort_by_title(self):
        """
        Test sorting tasks alphabetically by title.
        """
        sorted_tasks = self.service.sort_tasks("title", ascending=True)

        # Alpha should come first alphabetically
        self.assertEqual(sorted_tasks[0].title, "Alpha task")
        self.assertEqual(sorted_tasks[-1].title, "Zebra task")

    def test_sort_by_due_date(self):
        """
        Test sorting tasks by due date.
        """
        sorted_tasks = self.service.sort_tasks("due_date", ascending=True)

        # Earliest date should come first
        self.assertEqual(sorted_tasks[0].due_date, "2023-01-01")
        self.assertEqual(sorted_tasks[-1].due_date, "2023-12-31")


class TestCLIFunctionality(unittest.TestCase):
    """
    Acceptance tests for CLI functionality
    """

    def test_cli_add_command_with_priority(self):
        """
        Test the CLI add command with priority flag.
        """
        cli = TodoCLI()

        # Mock command line arguments for adding a task with priority
        with patch('sys.argv', ['todo_cli.py', 'add', 'Test task', '--priority', 'High']):
            # Capture stdout to prevent actual output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                cli.run()
            except SystemExit:
                pass  # argparse calls sys.exit when done
            finally:
                sys.stdout = sys.__stdout__  # Restore original stdout

    def test_cli_add_command_with_tags(self):
        """
        Test the CLI add command with tags flag.
        """
        cli = TodoCLI()

        # Mock command line arguments for adding a task with tags
        with patch('sys.argv', ['todo_cli.py', 'add', 'Test task', '--tags', 'work', 'urgent']):
            # Capture stdout to prevent actual output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                cli.run()
            except SystemExit:
                pass  # argparse calls sys.exit when done
            finally:
                sys.stdout = sys.__stdout__  # Restore original stdout


class TestRegressionPhase1(unittest.TestCase):
    """
    Regression tests to ensure Phase 1 functionality still works
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.service = TaskService()

    def test_add_task_basic(self):
        """
        Test basic task addition (Phase 1 functionality).
        """
        task = self.service.add_task("Basic task")
        self.assertEqual(task.title, "Basic task")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, "Medium")  # Default priority from new implementation
        self.assertEqual(task.tags, [])  # Default empty tags from new implementation
        self.assertIsNone(task.due_date)  # Default no due date from new implementation

    def test_list_all_tasks(self):
        """
        Test listing all tasks (Phase 1 functionality).
        """
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_task_by_id(self):
        """
        Test getting a specific task by ID (Phase 1 functionality).
        """
        task = self.service.add_task("Test task")
        retrieved_task = self.service.get_task_by_id(task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.title, "Test task")

    def test_update_task(self):
        """
        Test updating a task (Phase 1 functionality preserved).
        """
        task = self.service.add_task("Original task")
        success = self.service.update_task(task.id, title="Updated task")
        self.assertTrue(success)

        updated_task = self.service.get_task_by_id(task.id)
        self.assertEqual(updated_task.title, "Updated task")

    def test_complete_task(self):
        """
        Test marking a task as complete (Phase 1 functionality).
        """
        task = self.service.add_task("Test task")
        success = self.service.update_task(task.id, completed=True)
        self.assertTrue(success)

        completed_task = self.service.get_task_by_id(task.id)
        self.assertTrue(completed_task.completed)

    def test_delete_task(self):
        """
        Test deleting a task (Phase 1 functionality).
        """
        task = self.service.add_task("Test task")
        initial_count = len(self.service.get_all_tasks())

        success = self.service.delete_task(task.id)
        self.assertTrue(success)

        final_count = len(self.service.get_all_tasks())
        self.assertEqual(final_count, initial_count - 1)


if __name__ == '__main__':
    unittest.main()