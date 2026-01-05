"""
CLI interface for the todo application with extended functionality.

This module provides a command-line interface for managing tasks with
support for priorities, tags, search, filter, and sort functionality.
"""

import sys
import argparse
from typing import List, Optional
from src.services.task_service import TaskService
from src.task_models.task import Task


class TodoCLI:
    """
    Command-line interface for the todo application.
    """

    def __init__(self):
        """
        Initialize the CLI with a task service.
        """
        self.task_service = TaskService()

    def run(self):
        """
        Run the CLI application.
        """
        parser = argparse.ArgumentParser(description='Todo Application with Organization Features')
        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Add command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('title', help='Task title')
        add_parser.add_argument('--description', '-d', default='', help='Task description')
        add_parser.add_argument('--priority', '-p', choices=['High', 'Medium', 'Low'],
                               default='Medium', help='Task priority (default: Medium)')
        add_parser.add_argument('--tags', '-t', type=str, nargs='*', default=[],
                               help='Task tags (space-separated)')
        add_parser.add_argument('--due-date', help='Due date in YYYY-MM-DD format')

        # List command
        list_parser = subparsers.add_parser('list', help='List all tasks')
        list_parser.add_argument('--status', choices=['completed', 'incomplete'],
                                 help='Filter by completion status')
        list_parser.add_argument('--priority', choices=['High', 'Medium', 'Low'],
                                 help='Filter by priority')
        list_parser.add_argument('--tag', help='Filter by tag')
        list_parser.add_argument('--sort', choices=['due_date', 'priority', 'title'],
                                 help='Sort by field')
        list_parser.add_argument('--reverse', action='store_true',
                                 help='Reverse sort order')

        # Search command
        search_parser = subparsers.add_parser('search', help='Search tasks')
        search_parser.add_argument('keyword', help='Search keyword')

        # Complete command
        complete_parser = subparsers.add_parser('complete', help='Mark task as complete')
        complete_parser.add_argument('task_id', type=int, help='Task ID to complete')

        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('task_id', type=int, help='Task ID to delete')

        # Parse arguments
        args = parser.parse_args()

        # Execute command based on parsed arguments
        if args.command == 'add':
            self.handle_add(args)
        elif args.command == 'list':
            self.handle_list(args)
        elif args.command == 'search':
            self.handle_search(args)
        elif args.command == 'complete':
            self.handle_complete(args)
        elif args.command == 'delete':
            self.handle_delete(args)
        else:
            parser.print_help()

    def handle_add(self, args):
        """
        Handle the add command.
        """
        try:
            # Process tags - split comma-separated tags if provided as a single string
            tags = []
            for tag_arg in args.tags:
                if ',' in tag_arg:
                    # Handle comma-separated tags in a single argument
                    tags.extend([t.strip() for t in tag_arg.split(',') if t.strip()])
                else:
                    tags.append(tag_arg)

            # Remove duplicates while preserving order
            unique_tags = []
            for tag in tags:
                if tag not in unique_tags:
                    unique_tags.append(tag)

            task = self.task_service.add_task(
                title=args.title,
                description=args.description,
                priority=args.priority,
                tags=unique_tags,
                due_date=args.due_date
            )
            print(f"Task added successfully with ID {task.id}: {task}")
        except ValueError as e:
            print(f"Error adding task: {e}", file=sys.stderr)
            sys.exit(1)

    def handle_list(self, args):
        """
        Handle the list command with optional filtering and sorting.
        """
        try:
            # Get tasks with optional filtering
            tasks = self.task_service.get_tasks_filtered_and_sorted(
                status=args.status,
                priority=args.priority,
                tag=args.tag,
                sort_field=args.sort,
                ascending=not args.reverse
            )

            if not tasks:
                print("No tasks found.")
                return

            # Display tasks
            for task in tasks:
                print(task)
        except ValueError as e:
            print(f"Error listing tasks: {e}", file=sys.stderr)
            sys.exit(1)

    def handle_search(self, args):
        """
        Handle the search command.
        """
        try:
            tasks = self.task_service.search_tasks(args.keyword)

            if not tasks:
                print("No tasks found matching the search term.")
                return

            # Display search results
            print(f"Found {len(tasks)} task(s) matching '{args.keyword}':")
            for task in tasks:
                print(task)
        except ValueError as e:
            print(f"Error searching tasks: {e}", file=sys.stderr)
            sys.exit(1)

    def handle_complete(self, args):
        """
        Handle the complete command.
        """
        try:
            success = self.task_service.update_task(args.task_id, completed=True)
            if success:
                task = self.task_service.get_task_by_id(args.task_id)
                if task:
                    print(f"Task marked as complete: {task}")
                else:
                    print(f"Task {args.task_id} not found after update.")
            else:
                print(f"Task with ID {args.task_id} not found.")
                sys.exit(1)
        except ValueError as e:
            print(f"Error completing task: {e}", file=sys.stderr)
            sys.exit(1)

    def handle_delete(self, args):
        """
        Handle the delete command.
        """
        try:
            success = self.task_service.delete_task(args.task_id)
            if success:
                print(f"Task with ID {args.task_id} deleted successfully.")
            else:
                print(f"Task with ID {args.task_id} not found.")
                sys.exit(1)
        except Exception as e:
            print(f"Error deleting task: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """
    Main entry point for the CLI application.
    """
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()