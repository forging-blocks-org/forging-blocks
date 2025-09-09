from typing import Generic, Protocol, TypeVar

TNotification = TypeVar("TNotification", contravariant=True)


class Notifier(Protocol, Generic[TNotification]):
    """
    Asynchronous notifier interface for sending notifications.

    This interface defines the contract for sending notifications in an asynchronous
    manner.
    It can be implemented by various notification services, such as email, SMS
    or push notifications.
    """

    async def notify(self, message: TNotification) -> None:
        """
        Send a notification with the given message.

        Args:
            message: The message to be sent in the notification.
        """
        ...
