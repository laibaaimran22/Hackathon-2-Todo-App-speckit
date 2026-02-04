"""
Event handlers for the todo application
Handles incoming events from the event bus
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

from sqlmodel import Session, select
from sqlalchemy import func

from database import engine
from models import Task, User, Tag, TaskTagLink

logger = logging.getLogger(__name__)

class EventHandler:
    def __init__(self):
        self.session = Session(engine)

    async def handle_task_created(self, event_data: Dict[str, Any]):
        """Handle task.created event"""
        try:
            logger.info(f"Handling task.created event for task ID: {event_data.get('task_id')}")

            # Log the event for audit purposes
            task_id = event_data.get('task_id')
            user_id = event_data.get('user_id')
            title = event_data.get('title')

            print(f"[EVENT] Task created: {title} (ID: {task_id}) for user {user_id}")

            # Check if this is a recurring task
            recurrence_pattern = event_data.get('recurrence_pattern')
            if recurrence_pattern:
                await self._schedule_next_occurrence(event_data)

        except Exception as e:
            logger.error(f"Error handling task.created event: {e}")
            raise

    async def handle_task_updated(self, event_data: Dict[str, Any]):
        """Handle task.updated event"""
        try:
            logger.info(f"Handling task.updated event for task ID: {event_data.get('task_id')}")

            task_id = event_data.get('task_id')
            user_id = event_data.get('user_id')
            title = event_data.get('title')

            print(f"[EVENT] Task updated: {title} (ID: {task_id}) for user {user_id}")

            # Check if recurrence pattern was changed
            recurrence_pattern = event_data.get('recurrence_pattern')
            if recurrence_pattern:
                await self._schedule_next_occurrence(event_data)

        except Exception as e:
            logger.error(f"Error handling task.updated event: {e}")
            raise

    async def handle_task_completed(self, event_data: Dict[str, Any]):
        """Handle task.completed event"""
        try:
            logger.info(f"Handling task.completed event for task ID: {event_data.get('task_id')}")

            task_id = event_data.get('task_id')
            user_id = event_data.get('user_id')
            title = event_data.get('title')

            print(f"[EVENT] Task completed: {title} (ID: {task_id}) for user {user_id}")

            # Check if this was a recurring task and create the next occurrence
            task = self.session.get(Task, task_id)
            if task and task.recurrence_pattern:
                await self._create_next_occurrence(task)

        except Exception as e:
            logger.error(f"Error handling task.completed event: {e}")
            raise

    async def handle_task_deleted(self, event_data: Dict[str, Any]):
        """Handle task.deleted event"""
        try:
            logger.info(f"Handling task.deleted event for task ID: {event_data.get('task_id')}")

            task_id = event_data.get('task_id')
            user_id = event_data.get('user_id')
            title = event_data.get('title')

            print(f"[EVENT] Task deleted: {title} (ID: {task_id}) for user {user_id}")

        except Exception as e:
            logger.error(f"Error handling task.deleted event: {e}")
            raise

    async def handle_task_reminder(self, event_data: Dict[str, Any]):
        """Handle task.reminder event"""
        try:
            logger.info(f"Handling task.reminder event for task ID: {event_data.get('task_id')}")

            task_id = event_data.get('task_id')
            user_id = event_data.get('user_id')
            title = event_data.get('title')
            due_date = event_data.get('due_date')

            print(f"[EVENT] Reminder for task: {title} (ID: {task_id}) due on {due_date}")

            # In a real implementation, this would send an email notification
            # For now, just log it
            print(f"[NOTIFICATION] Would send reminder email to user {user_id} about task {title}")

        except Exception as e:
            logger.error(f"Error handling task.reminder event: {e}")
            raise

    async def _create_next_occurrence(self, original_task: Task):
        """Create the next occurrence of a recurring task"""
        try:
            # Determine the next due date based on the recurrence pattern
            next_due_date = self._calculate_next_date(original_task.due_date, original_task.recurrence_pattern)

            if next_due_date:
                # Create a new task with the same properties as the original
                new_task = Task(
                    title=original_task.title,
                    description=original_task.description,
                    priority=original_task.priority,
                    due_date=next_due_date,
                    recurrence_pattern=original_task.recurrence_pattern,
                    owner_id=original_task.owner_id,
                    is_completed=False
                )

                self.session.add(new_task)
                self.session.commit()
                self.session.refresh(new_task)

                print(f"[RECURRING] Created next occurrence of task '{original_task.title}' (ID: {new_task.id}) due on {next_due_date}")

                # Copy tags from the original task to the new task
                original_task_tags = self.session.exec(
                    select(Tag).join(TaskTagLink).where(TaskTagLink.task_id == original_task.id)
                ).all()

                for tag in original_task_tags:
                    task_tag_link = TaskTagLink(task_id=new_task.id, tag_id=tag.id)
                    self.session.add(task_tag_link)

                self.session.commit()

        except Exception as e:
            logger.error(f"Error creating next occurrence for task {original_task.id}: {e}")
            raise

    def _calculate_next_date(self, due_date: datetime, recurrence_pattern: str) -> datetime:
        """Calculate the next date based on the recurrence pattern"""
        if not due_date or not recurrence_pattern:
            return None

        if recurrence_pattern == "daily":
            return due_date + timedelta(days=1)
        elif recurrence_pattern == "weekly":
            return due_date + timedelta(weeks=1)
        elif recurrence_pattern == "monthly":
            # For monthly, we'll add approximately one month (30 days)
            # In a real implementation, you'd want to handle month boundaries properly
            return due_date + timedelta(days=30)
        else:
            return None

    async def _schedule_next_occurrence(self, event_data: Dict[str, Any]):
        """Schedule the next occurrence for recurring tasks"""
        try:
            # This would typically schedule a delayed message or use a scheduler
            # For now, we'll just log that scheduling happened
            task_id = event_data.get('task_id')
            recurrence_pattern = event_data.get('recurrence_pattern')
            due_date = event_data.get('due_date')

            if recurrence_pattern and due_date:
                next_date = self._calculate_next_date(datetime.fromisoformat(due_date.replace('Z', '+00:00')), recurrence_pattern)
                print(f"[SCHEDULER] Scheduled next occurrence for task {task_id} on {next_date}")

        except Exception as e:
            logger.error(f"Error scheduling next occurrence: {e}")
            raise

    async def check_due_tasks_and_send_reminders(self):
        """Check for tasks that are due soon and send reminders"""
        try:
            # Find tasks that are due within the next 24 hours and are not completed
            now = datetime.now()
            tomorrow = now + timedelta(hours=24)

            due_soon_tasks = self.session.exec(
                select(Task)
                .where(Task.due_date <= tomorrow)
                .where(Task.due_date >= now)
                .where(Task.is_completed == False)
            ).all()

            for task in due_soon_tasks:
                print(f"[REMINDER-CHECK] Task '{task.title}' is due soon on {task.due_date}")

                # Publish reminder event
                reminder_event = {
                    "task_id": task.id,
                    "user_id": task.owner_id,
                    "title": task.title,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "reminder_time": now.isoformat()
                }

                # In a real implementation, you'd publish this to the event bus
                print(f"[EVENT-PUBLISH] Publishing task.reminder event for task {task.id}")

        except Exception as e:
            logger.error(f"Error checking due tasks: {e}")
            raise

    def close(self):
        """Close the database session"""
        if self.session:
            self.session.close()

# Global event handler instance
event_handler = EventHandler()

# Example of how this might be used in a background task
async def run_scheduler():
    """Background task to periodically check for due tasks and send reminders"""
    while True:
        try:
            await event_handler.check_due_tasks_and_send_reminders()
            await asyncio.sleep(3600)  # Check every hour
        except Exception as e:
            logger.error(f"Error in scheduler: {e}")
            await asyncio.sleep(300)  # Wait 5 minutes before retrying