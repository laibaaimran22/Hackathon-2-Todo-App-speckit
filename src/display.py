"""
In-Memory Todo Console Application
Display and output formatting module
"""
from typing import List
from models import Task


class Display:
    def show_menu(self):
        """Display the main menu options"""
        print("\n" + "="*40)
        print("TODO APPLICATION - MAIN MENU")
        print("="*40)
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Update an existing task")
        print("4. Delete a task")
        print("5. Mark task as complete/incomplete")
        print("6. Exit")
        print("="*40)

    def show_tasks(self, tasks: List[Task]):
        """Display all tasks with clear status indicators"""
        if not tasks:
            print("\nNo tasks found. Your todo list is empty!")
            return

        print("\n" + "="*60)
        print("YOUR TASKS")
        print("="*60)

        for task in tasks:
            status_indicator = "✓" if task["completed"] else "○"
            status_text = "Complete" if task["completed"] else "Incomplete"

            print(f"ID: {task['id']}")
            print(f"Status: [{status_indicator}] {status_text}")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description'] if task['description'] else '[No description]'}")
            print("-" * 60)