"""
Unit tests for the updated Task model using TypedDict approach.
"""
import unittest
from src.models import Task


class TestTaskTypedDict(unittest.TestCase):
    """
    Unit tests for the Task TypedDict.
    """

    def test_task_structure(self):
        """
        Test that Task TypedDict has the expected structure.
        """
        # Create a sample task dictionary that matches the TypedDict
        task: Task = {
            'id': 1,
            'title': 'Test Task',
            'description': 'Test Description',
            'completed': False,
            'priority': 'Medium',
            'tags': ['work', 'important'],
            'due_date': '2024-12-31'
        }

        self.assertEqual(task['id'], 1)
        self.assertEqual(task['title'], 'Test Task')
        self.assertEqual(task['description'], 'Test Description')
        self.assertEqual(task['completed'], False)
        self.assertEqual(task['priority'], 'Medium')
        self.assertEqual(task['tags'], ['work', 'important'])
        self.assertEqual(task['due_date'], '2024-12-31')


if __name__ == '__main__':
    unittest.main()