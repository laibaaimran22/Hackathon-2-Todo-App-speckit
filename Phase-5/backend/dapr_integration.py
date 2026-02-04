"""
Dapr integration for the todo application
Handles event publishing and subscribing for the event-driven architecture
"""
import json
import logging
from typing import Dict, Any
from datetime import datetime

from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem

logger = logging.getLogger(__name__)

class DaprIntegration:
    def __init__(self):
        self.client = None
        self.pubsub_name = "task-pubsub"

    def initialize(self):
        """Initialize the Dapr client"""
        try:
            self.client = DaprClient()
            logger.info("Dapr client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Dapr client: {e}")
            raise

    def publish_task_event(self, event_type: str, task_data: Dict[str, Any]):
        """Publish a task-related event to the event bus"""
        if not self.client:
            logger.warning("Dapr client not initialized, skipping event publish")
            return

        try:
            # Add timestamp to the event
            event_payload = {
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "task_data": task_data
            }

            # Publish to the appropriate topic based on event type
            topic_name = self._get_topic_for_event(event_type)

            self.client.publish_event(
                pubsub_name=self.pubsub_name,
                topic_name=topic_name,
                data=json.dumps(event_payload),
                data_content_type='application/json'
            )

            logger.info(f"Published event '{event_type}' to topic '{topic_name}'")
        except Exception as e:
            logger.error(f"Failed to publish event '{event_type}': {e}")
            raise

    def _get_topic_for_event(self, event_type: str) -> str:
        """Map event types to appropriate topics"""
        topic_mapping = {
            "task.created": "task-created",
            "task.updated": "task-updated",
            "task.completed": "task-completed",
            "task.deleted": "task-deleted",
            "task.reminder": "task-reminder",
            "task.recurring": "task-recurring"
        }
        return topic_mapping.get(event_type, "task-events")

    def save_state(self, key: str, value: Any):
        """Save state using Dapr state store"""
        if not self.client:
            logger.warning("Dapr client not initialized, skipping state save")
            return

        try:
            state_value = json.dumps(value) if not isinstance(value, str) else value
            self.client.save_state(
                store_name="task-statestore",
                key=key,
                value=state_value
            )
            logger.info(f"Saved state for key: {key}")
        except Exception as e:
            logger.error(f"Failed to save state for key '{key}': {e}")
            raise

    def get_state(self, key: str) -> Any:
        """Get state from Dapr state store"""
        if not self.client:
            logger.warning("Dapr client not initialized, returning None")
            return None

        try:
            response = self.client.get_state(
                store_name="task-statestore",
                key=key
            )
            if response.data:
                return json.loads(response.data.decode('utf-8'))
            return None
        except Exception as e:
            logger.error(f"Failed to get state for key '{key}': {e}")
            return None

    def close(self):
        """Close the Dapr client"""
        if self.client:
            self.client.close()

# Global instance for use in the application
dapr_client = DaprIntegration()