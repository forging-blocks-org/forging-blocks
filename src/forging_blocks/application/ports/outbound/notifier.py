"""Outbound port defining an asynchronous notification service.

A Notifier provides an abstraction for sending notification messages using
external delivery channels such as email, SMS, chat systems, or push
notifications.

Responsibilities:
    - Send notification messages asynchronously.

Non-Responsibilities:
    - Guarantee delivery.
    - Implement retries or throttling unless defined by infrastructure.
"""

from typing import Generic, Protocol, TypeVar

from forging_blocks.foundation.ports import OutboundPort

NotificationType = TypeVar("NotificationType", contravariant=True)


class Notifier(
    OutboundPort[NotificationType, None], Generic[NotificationType], Protocol
):
    """Outbound port for sending asynchronous notifications.

    Implementers integrate with concrete notification systems. The
    application layer must not depend on infrastructure details beyond this
    abstraction.
    """

    async def notify(self, message: NotificationType) -> None:
        """Send a notification.

        Args:
            message: The message to deliver.

        Notes:
            - Fire-and-forget behavior unless documented otherwise.
            - Delivery semantics are infrastructure-defined.
        """
        ...
