"""
Unit tests for the Task model.

This module tests the Task model with extended functionality
including priorities, tags, and due dates.
"""

import unittest
from src.task_models.task import Task


class TestTask(unittest.TestCase):
    """
    Unit tests for the Task class.
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.task = Task(1, "Test Task", "Test Description")

    def test_task_initialization(self):
        """
        Test that a task is properly initialized with default values.
        """
        self.assertEqual(self.task.id, 1)
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertEqual(self.task.completed, False)
        self.assertEqual(self.task.priority, "Medium")  # Default priority
        self.assertEqual(self.task.tags, [])  # Default empty tags list
        self.assertEqual(self.task.due_date, None)  # Default no due date

    def test_set_priority_valid(self):
        """
        Test setting valid priority levels.
        """
        self.task.set_priority("High")
        self.assertEqual(self.task.priority, "High")

        self.task.set_priority("Medium")
        self.assertEqual(self.task.priority, "Medium")

        self.task.set_priority("Low")
        self.assertEqual(self.task.priority, "Low")

    def test_set_priority_invalid(self):
        """
        Test that setting an invalid priority raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.task.set_priority("Invalid")

        with self.assertRaises(ValueError):
            self.task.set_priority("HIGH")  # Case sensitive

    def test_add_tag(self):
        """
        Test adding tags to a task.
        """
        self.task.add_tag("work")
        self.assertIn("work", self.task.tags)
        self.assertEqual(len(self.task.tags), 1)

        self.task.add_tag("urgent")
        self.assertIn("urgent", self.task.tags)
        self.assertEqual(len(self.task.tags), 2)

        # Adding the same tag should not duplicate
        self.task.add_tag("work")
        self.assertEqual(len(self.task.tags), 2)  # Still only 2 tags

    def test_add_tag_invalid(self):
        """
        Test that adding invalid tags raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.task.add_tag("")  # Empty tag

        with self.assertRaises(ValueError):
            self.task.add_tag("   ")  # Whitespace only

        with self.assertRaises(ValueError):
            self.task.add_tag(None)  # None value (though this would cause TypeError)

    def test_remove_tag(self):
        """
        Test removing tags from a task.
        """
        self.task.add_tag("work")
        self.task.add_tag("personal")

        # Remove existing tag
        result = self.task.remove_tag("work")
        self.assertTrue(result)
        self.assertNotIn("work", self.task.tags)
        self.assertIn("personal", self.task.tags)

        # Remove non-existing tag
        result = self.task.remove_tag("work")  # Already removed
        self.assertFalse(result)

    def test_set_due_date_valid(self):
        """
        Test setting valid due dates.
        """
        self.task.set_due_date("2023-12-31")
        self.assertEqual(self.task.due_date, "2023-12-31")

        self.task.set_due_date(None)
        self.assertIsNone(self.task.due_date)

    def test_set_due_date_invalid(self):
        """
        Test that setting invalid due dates raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.task.set_due_date("invalid-date")

        with self.assertRaises(ValueError):
            self.task.set_due_date("2023/12/31")  # Wrong format

        with self.assertRaises(ValueError):
            self.task.set_due_date("2023-13-01")  # Invalid month

        with self.assertRaises(ValueError):
            self.task.set_due_date("2023-12-32")  # Invalid day

    def test_to_dict(self):
        """
        Test converting task to dictionary.
        """
        self.task.set_priority("High")
        self.task.add_tag("work")
        self.task.set_due_date("2023-12-31")

        task_dict = self.task.to_dict()
        expected = {
            'id': 1,
            'title': 'Test Task',
            'description': 'Test Description',
            'completed': False,
            'priority': 'High',
            'tags': ['work'],
            'due_date': '2023-12-31'
        }

        self.assertEqual(task_dict, expected)

    def test_str_representation(self):
        """
        Test string representation of the task.
        """
        # Test incomplete task
        self.task.set_priority("High")
        self.task.add_tag("work")
        self.task.set_due_date("2023-12-31")
        expected = "[O] 1: Test Task [High] [work] (due: 2023-12-31)"
        self.assertEqual(str(self.task), expected)

        # Test completed task
        self.task.completed = True
        expected = "[X] 1: Test Task [High] [work] (due: 2023-12-31)"
        self.assertEqual(str(self.task), expected)

        # Test task without tags or due date
        simple_task = Task(2, "Simple Task")
        expected = "[O] 2: Simple Task [Medium]"
        self.assertEqual(str(simple_task), expected)


if __name__ == '__main__':
    unittest.main()