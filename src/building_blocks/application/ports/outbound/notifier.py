"""Asynchronous notifier interface for sending notifications."""

from typing import Generic, Protocol, TypeVar

NotificationType = TypeVar("NotificationType", contravariant=True)


class Notifier(Protocol, Generic[NotificationType]):
    """Asynchronous notifier interface for sending notifications.

    This interface defines the contract for sending notifications in an asynchronous
    manner.
    It can be implemented by various notification services, such as email, SMS
    or push notifications.
    """

    async def notify(self, message: NotificationType) -> None:
        """Send a notification with the given message.

        Args:
            message: The message to be sent in the notification.
        """
        ...
