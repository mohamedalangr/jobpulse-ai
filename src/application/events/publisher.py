import logging
from src.application.events.base import Event

logger = logging.getLogger(__name__)

class EventPublisher:
    def publish(self, event: Event) -> None:
        # Currently just logs. Ready for Redis/Kafka integration in the future.
        logger.info(f"EventPublished: {event.__class__.__name__} [correlation_id={event.correlation_id}] payload={event}")
