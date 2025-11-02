"""Notifier module.

Auto-generated minimal module docstring.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TNotification = TypeVar("TNotification")


class AsyncNotifier(ABC, Generic[TNotification]):
    """Asynchronous notifier interface for sending notifications.

    This interface defines the contract for sending notifications in an asynchronous
    manner.
    It can be implemented by various notification services, such as email, SMS
    or push notifications.
    """

    @abstractmethod
    async def notify(self, message: TNotification) -> None:
        """Send a notification with the given message.

        Args:
            message: The message to be sent in the notification.
        """
        pass


class SyncNotifier(ABC, Generic[TNotification]):
    """Synchronous notifier interface for sending notifications.

    This interface defines the contract for sending notifications in a sync
    manner.
    It can be implemented by various notification services, such as email, SMS
    or push notifications.
    """

    @abstractmethod
    def notify(self, message: TNotification) -> None:
        """Send a notification with the given message.

        Args:
            message: The message to be sent in the notification.
        """
        pass
