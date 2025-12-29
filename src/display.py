"""
In-Memory Todo Console Application
Display and output formatting module with extended functionality
"""
from typing import List
from models import Task


class Display:
    def show_menu(self):
        """Display the main menu options"""
        print("\n" + "="*60)
        print("TODO APPLICATION - MAIN MENU")
        print("="*60)
        print("1.  Add a new task")
        print("2.  View all tasks")
        print("3.  Update an existing task")
        print("4.  Delete a task")
        print("5.  Mark task as complete/incomplete")
        print("6.  Search tasks")
        print("7.  Filter tasks")
        print("8.  Sort tasks")
        print("9.  View overdue tasks")
        print("10. View upcoming tasks")
        print("11. Add a recurring task")
        print("12. Exit")
        print("="*60)

    def show_tasks(self, tasks: List[Task]):
        """Display all tasks with clear status indicators and extended information"""
        if not tasks:
            print("\nNo tasks found. Your todo list is empty!")
            return

        print("\n" + "="*100)
        print("YOUR TASKS")
        print("="*100)

        for task in tasks:
            status_indicator = "X" if task["completed"] else "O"
            status_text = "Complete" if task["completed"] else "Incomplete"
            priority = task["priority"]
            tags = ", ".join(task["tags"]) if task["tags"] else "No tags"
            due_date = task["due_date"] if task["due_date"] else "No due date"

            # Determine due date status
            due_status = ""
            if task["due_date"]:
                # Calculate due status - we'll use a simple approach here since we don't have access to the task manager
                try:
                    from datetime import datetime
                    due_date_obj = datetime.strptime(task["due_date"], '%Y-%m-%d')
                    current_date = datetime.now().date()
                    due_date_only = due_date_obj.date()

                    if due_date_only < current_date:
                        due_status = " (OVERDUE)"
                    elif due_date_only == current_date:
                        due_status = " (TODAY)"
                    else:
                        due_status = " (UPCOMING)"
                except ValueError:
                    due_status = ""

            # Show recurrence information
            recurrence_info = ""
            if task.get("recurrence_pattern"):
                recurrence_info = f" [Recurring: {task['recurrence_pattern']}]"

            print(f"ID: {task['id']}")
            print(f"Status: [{status_indicator}] {status_text}")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description'] if task['description'] else '[No description]'}")
            print(f"Priority: {priority}")
            print(f"Tags: {tags}")
            print(f"Due Date: {due_date}{due_status}")
            print(f"Recurrence: {task['recurrence_pattern'] if task['recurrence_pattern'] else 'None'}{recurrence_info}")
            print("-" * 100)

    def show_search_prompt(self):
        """Prompt user for search keyword"""
        print("\n" + "-"*40)
        print("SEARCH TASKS")
        print("-"*40)
        keyword = input("Enter keyword to search (in title or description): ").strip()
        return keyword

    def show_filter_prompt(self):
        """Prompt user for filter options"""
        print("\n" + "-"*40)
        print("FILTER TASKS")
        print("-"*40)
        print("Filter by status (leave blank to skip):")
        print("  'completed' or 'incomplete'")
        status = input("Status: ").strip().lower()
        if status and status not in ["completed", "incomplete"]:
            print("Invalid status. Use 'completed' or 'incomplete'.")
            return None, None, None

        print("\nFilter by priority (leave blank to skip):")
        print("  'High', 'Medium', or 'Low'")
        priority = input("Priority: ").strip().title()
        if priority and priority not in ["High", "Medium", "Low"]:
            print("Invalid priority. Use 'High', 'Medium', or 'Low'.")
            return None, None, None

        print("\nFilter by tag (leave blank to skip):")
        tag = input("Tag: ").strip()

        return status, priority, tag

    def show_sort_prompt(self):
        """Prompt user for sort options"""
        print("\n" + "-"*40)
        print("SORT TASKS")
        print("-"*40)
        print("Sort by field:")
        print("  'title', 'priority', or 'due_date'")
        sort_field = input("Sort field: ").strip().lower()
        if sort_field not in ["title", "priority", "due_date"]:
            print("Invalid sort field. Use 'title', 'priority', or 'due_date'.")
            return None, True

        ascending_input = input("Ascending order? (y/n, default y): ").strip().lower()
        ascending = ascending_input != 'n'

        return sort_field, ascending