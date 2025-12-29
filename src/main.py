"""
In-Memory Todo Console Application
Entry point and CLI interface module with extended functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from task_manager import TaskManager
from display import Display
import sys


class TodoApp:
    def __init__(self):
        self.task_manager = TaskManager()
        self.display = Display()

    def run(self):
        """Main application loop"""
        print("Welcome to the In-Memory Todo Console Application!")
        print("All data will be lost when you exit the application.")

        while True:
            self.display.show_menu()
            choice = input("Select an option (1-12): ").strip()

            if choice == '1':
                self._add_task()
            elif choice == '2':
                self._view_tasks()
            elif choice == '3':
                self._update_task()
            elif choice == '4':
                self._delete_task()
            elif choice == '5':
                self._mark_task_status()
            elif choice == '6':
                self._search_tasks()
            elif choice == '7':
                self._filter_tasks()
            elif choice == '8':
                self._sort_tasks()
            elif choice == '9':
                self._view_overdue_tasks()
            elif choice == '10':
                self._view_upcoming_tasks()
            elif choice == '11':
                self._add_recurring_task()
            elif choice == '12':
                print("Thank you for using the Todo Application. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid option, please try again.")

    def _add_task(self):
        """Handle adding a new task with extended functionality"""
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Title is required!")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()

            print("Enter priority (High/Medium/Low, default: Medium): ")
            priority = input().strip().title()
            if not priority:
                priority = "Medium"
            elif priority not in ["High", "Medium", "Low"]:
                print("Invalid priority. Using 'Medium' as default.")
                priority = "Medium"

            tags_input = input("Enter tags separated by commas (optional, press Enter to skip): ").strip()
            tags = []
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

            due_date = input("Enter due date (YYYY-MM-DD format, optional, press Enter to skip): ").strip()
            if not due_date:
                due_date = None

            # Ask if user wants to set up recurrence
            print("Set up recurrence? (y/n, default: n): ")
            recurrence_choice = input().strip().lower()
            recurrence_pattern = None
            recurrence_interval = 1

            if recurrence_choice in ['y', 'yes']:
                print("Enter recurrence pattern (daily/weekly/monthly, optional, press Enter to skip): ")
                recurrence_pattern = input().strip().lower()
                if recurrence_pattern and recurrence_pattern not in ["daily", "weekly", "monthly"]:
                    print("Invalid recurrence pattern. Valid options: daily, weekly, monthly")
                    recurrence_pattern = None
                elif not recurrence_pattern:
                    recurrence_pattern = None

                if recurrence_pattern:
                    interval_input = input("Enter recurrence interval (number of units, default: 1): ").strip()
                    try:
                        recurrence_interval = int(interval_input) if interval_input else 1
                        if recurrence_interval <= 0:
                            print("Invalid interval. Using default of 1.")
                            recurrence_interval = 1
                    except ValueError:
                        print("Invalid interval. Using default of 1.")
                        recurrence_interval = 1

            task = self.task_manager.add_task(
                title, description, priority, tags, due_date,
                recurrence_pattern, recurrence_interval
            )
            print(f"Task added successfully with ID: {task['id']}")
            if recurrence_pattern:
                print(f"Task will repeat {recurrence_pattern} with interval {recurrence_interval}")
        except Exception as e:
            print(f"Error adding task: {str(e)}")

    def _view_tasks(self):
        """Handle viewing all tasks"""
        try:
            tasks = self.task_manager.get_all_tasks()
            self.display.show_tasks(tasks)
        except Exception as e:
            print(f"Error viewing tasks: {str(e)}")

    def _update_task(self):
        """Handle updating an existing task with extended functionality"""
        try:
            task_id_str = input("Enter task ID to update: ").strip()
            if not task_id_str.isdigit():
                print("Invalid task ID. Please enter a number.")
                return

            task_id = int(task_id_str)
            task = self.task_manager.get_task_by_id(task_id)
            if not task:
                print(f"Task with ID {task_id} not found.")
                return

            print(f"Current title: {task['title']}")
            new_title = input("Enter new title (press Enter to keep current): ").strip()
            if new_title == "":
                new_title = task['title']

            print(f"Current description: {task['description']}")
            new_description = input("Enter new description (press Enter to keep current): ").strip()
            if new_description == "":
                new_description = task['description']

            print(f"Current priority: {task['priority']}")
            new_priority = input("Enter new priority (High/Medium/Low, press Enter to keep current): ").strip().title()
            if new_priority == "":
                new_priority = task['priority']

            print(f"Current tags: {', '.join(task['tags']) if task['tags'] else 'No tags'}")
            tags_input = input("Enter new tags separated by commas (press Enter to keep current): ").strip()
            if tags_input == "":
                new_tags = None  # Use None to indicate no change
            else:
                new_tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

            print(f"Current due date: {task['due_date'] if task['due_date'] else 'No due date'}")
            new_due_date = input("Enter new due date (YYYY-MM-DD format, press Enter to keep current): ").strip()
            if new_due_date == "":
                new_due_date = None  # Use None to indicate no change

            print(f"Current recurrence pattern: {task['recurrence_pattern'] if task['recurrence_pattern'] else 'None'}")
            new_recurrence_pattern = input("Enter new recurrence pattern (daily/weekly/monthly, press Enter to keep current): ").strip().lower()
            if new_recurrence_pattern == "":
                new_recurrence_pattern = task['recurrence_pattern']
            elif new_recurrence_pattern and new_recurrence_pattern not in ["daily", "weekly", "monthly"]:
                print("Invalid recurrence pattern. Keeping current value.")
                new_recurrence_pattern = task['recurrence_pattern']

            print(f"Current recurrence interval: {task['recurrence_interval'] if task['recurrence_interval'] else '1'}")
            new_recurrence_interval = input("Enter new recurrence interval (press Enter to keep current): ").strip()
            if new_recurrence_interval == "":
                new_recurrence_interval = task['recurrence_interval']
            else:
                try:
                    new_recurrence_interval = int(new_recurrence_interval)
                    if new_recurrence_interval <= 0:
                        print("Invalid interval. Using current value.")
                        new_recurrence_interval = task['recurrence_interval']
                except ValueError:
                    print("Invalid interval. Using current value.")
                    new_recurrence_interval = task['recurrence_interval']

            updated_task = self.task_manager.update_task(
                task_id, new_title, new_description, new_priority, new_tags, new_due_date,
                new_recurrence_pattern, new_recurrence_interval
            )
            if updated_task:
                print(f"Task {task_id} updated successfully.")
            else:
                print("Error updating task.")
        except Exception as e:
            print(f"Error updating task: {str(e)}")

    def _delete_task(self):
        """Handle deleting a task"""
        try:
            task_id_str = input("Enter task ID to delete: ").strip()
            if not task_id_str.isdigit():
                print("Invalid task ID. Please enter a number.")
                return

            task_id = int(task_id_str)
            success = self.task_manager.delete_task(task_id)
            if success:
                print(f"Task {task_id} deleted successfully.")
            else:
                print(f"Task with ID {task_id} not found.")
        except Exception as e:
            print(f"Error deleting task: {str(e)}")

    def _mark_task_status(self):
        """Handle marking task as complete/incomplete"""
        try:
            task_id_str = input("Enter task ID to update status: ").strip()
            if not task_id_str.isdigit():
                print("Invalid task ID. Please enter a number.")
                return

            task_id = int(task_id_str)
            task = self.task_manager.get_task_by_id(task_id)
            if not task:
                print(f"Task with ID {task_id} not found.")
                return

            current_status = "Complete" if task['completed'] else "Incomplete"
            print(f"Current status: {current_status}")

            status_choice = input("Mark as (1) Complete or (2) Incomplete: ").strip()
            if status_choice == '1':
                completed = True
            elif status_choice == '2':
                completed = False
            else:
                print("Invalid choice. Please enter 1 or 2.")
                return

            updated_task = self.task_manager.mark_task_status(task_id, completed)
            if updated_task:
                new_status = "Complete" if completed else "Incomplete"
                print(f"Task {task_id} marked as {new_status}.")
            else:
                print("Error updating task status.")
        except Exception as e:
            print(f"Error marking task status: {str(e)}")

    def _search_tasks(self):
        """Handle searching tasks by keyword"""
        try:
            keyword = self.display.show_search_prompt()
            if not keyword:
                print("Search keyword cannot be empty.")
                return

            tasks = self.task_manager.search_tasks(keyword)
            if tasks:
                print(f"\nFound {len(tasks)} matching task(s):")
                self.display.show_tasks(tasks)
            else:
                print(f"No tasks found matching '{keyword}'.")
        except Exception as e:
            print(f"Error searching tasks: {str(e)}")

    def _filter_tasks(self):
        """Handle filtering tasks by status, priority, or tag"""
        try:
            status, priority, tag = self.display.show_filter_prompt()

            # Only apply filters that were specified by the user
            filtered_tasks = self.task_manager.filter_tasks(
                status=status if status else None,
                priority=priority if priority else None,
                tag=tag if tag else None
            )

            if filtered_tasks:
                print(f"\nFound {len(filtered_tasks)} filtered task(s):")
                self.display.show_tasks(filtered_tasks)
            else:
                print("No tasks match the specified filters.")
        except Exception as e:
            print(f"Error filtering tasks: {str(e)}")

    def _sort_tasks(self):
        """Handle sorting tasks by specified field"""
        try:
            sort_field, ascending = self.display.show_sort_prompt()

            if sort_field is None:
                print("Invalid sort parameters.")
                return

            sorted_tasks = self.task_manager.sort_tasks(sort_field, ascending)
            if sorted_tasks:
                print(f"\nTasks sorted by {sort_field} ({'ascending' if ascending else 'descending'}):")
                self.display.show_tasks(sorted_tasks)
            else:
                print("No tasks to display after sorting.")
        except Exception as e:
            print(f"Error sorting tasks: {str(e)}")

    def _view_overdue_tasks(self):
        """Handle viewing overdue tasks"""
        try:
            overdue_tasks = self.task_manager.get_overdue_tasks()
            if overdue_tasks:
                print(f"\nFound {len(overdue_tasks)} overdue task(s):")
                self.display.show_tasks(overdue_tasks)
            else:
                print("\nNo overdue tasks found.")
        except Exception as e:
            print(f"Error viewing overdue tasks: {str(e)}")

    def _view_upcoming_tasks(self):
        """Handle viewing upcoming tasks"""
        try:
            # Ask user for number of days to look ahead
            days_input = input("How many days ahead to check for upcoming tasks? (default 7): ").strip()
            try:
                days = int(days_input) if days_input else 7
            except ValueError:
                days = 7
                print("Invalid input. Using default of 7 days.")

            upcoming_tasks = self.task_manager.get_upcoming_tasks(days)
            if upcoming_tasks:
                print(f"\nFound {len(upcoming_tasks)} upcoming task(s) within {days} days:")
                self.display.show_tasks(upcoming_tasks)
            else:
                print(f"\nNo upcoming tasks found within {days} days.")
        except Exception as e:
            print(f"Error viewing upcoming tasks: {str(e)}")

    def _add_recurring_task(self):
        """Handle adding a recurring task"""
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Title is required!")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()

            print("Enter priority (High/Medium/Low, default: Medium): ")
            priority = input().strip().title()
            if not priority:
                priority = "Medium"
            elif priority not in ["High", "Medium", "Low"]:
                print("Invalid priority. Using 'Medium' as default.")
                priority = "Medium"

            tags_input = input("Enter tags separated by commas (optional, press Enter to skip): ").strip()
            tags = []
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

            due_date = input("Enter due date (YYYY-MM-DD format, optional, press Enter to skip): ").strip()
            if not due_date:
                due_date = None

            print("Enter recurrence pattern (daily/weekly/monthly, optional, press Enter to skip): ")
            recurrence_pattern = input().strip().lower()
            if recurrence_pattern and recurrence_pattern not in ["daily", "weekly", "monthly"]:
                print("Invalid recurrence pattern. Valid options: daily, weekly, monthly")
                return
            elif not recurrence_pattern:
                recurrence_pattern = None

            recurrence_interval = 1
            if recurrence_pattern:
                interval_input = input("Enter recurrence interval (number of units, default: 1): ").strip()
                try:
                    recurrence_interval = int(interval_input) if interval_input else 1
                    if recurrence_interval <= 0:
                        print("Invalid interval. Using default of 1.")
                        recurrence_interval = 1
                except ValueError:
                    print("Invalid interval. Using default of 1.")
                    recurrence_interval = 1

            task = self.task_manager.add_task(
                title, description, priority, tags, due_date,
                recurrence_pattern, recurrence_interval
            )
            print(f"Recurring task added successfully with ID: {task['id']}")
            if recurrence_pattern:
                print(f"Task will repeat {recurrence_pattern} with interval {recurrence_interval}")

        except Exception as e:
            print(f"Error adding recurring task: {str(e)}")


def main():
    """Application entry point"""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()