"""
In-Memory Todo Console Application
Entry point and CLI interface module
"""
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
            choice = input("Select an option (1-6): ").strip()

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
                print("Thank you for using the Todo Application. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid option, please try again.")

    def _add_task(self):
        """Handle adding a new task"""
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Title is required!")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()

            task = self.task_manager.add_task(title, description)
            print(f"Task added successfully with ID: {task['id']}")
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
        """Handle updating an existing task"""
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

            updated_task = self.task_manager.update_task(task_id, new_title, new_description)
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


def main():
    """Application entry point"""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()