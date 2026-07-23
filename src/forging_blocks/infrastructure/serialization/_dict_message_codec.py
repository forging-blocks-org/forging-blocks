"""Dict-based message codec that serializes messages to ``dict[str, object]``."""

from datetime import datetime
from typing import cast
from uuid import UUID

from forging_blocks.foundation.messages import Message, MessageMetadata

from ._message_codec import MessageCodec


class DictMessageCodec[M: Message[dict[str, object]]](MessageCodec[M, dict[str, object]]):
    """Codec that serializes messages to ``dict[str, object]``.

    Uses the message's own ``value`` property for the payload and
    ``message.metadata.value`` for the metadata section.  Reconstruction
    goes through the ``from_payload_fields`` classmethod that every
    concrete ``Message`` subclass provides.
    """

    def _to_data(self, message: M) -> dict[str, object]:
        """Serialize *message* to a dictionary.

        Returns a ``dict`` with ``metadata`` and ``payload`` keys.
        """
        return {
            "metadata": message.metadata.value,
            "payload": message.value,
        }

    def _from_data(self, data: dict[str, object], message_type: type[M]) -> M:
        """Reconstruct a message of *message_type* from *data*.

        Expects a ``dict`` with ``metadata`` and ``payload`` keys.
        """
        raw_metadata = cast(dict[str, object], data["metadata"])
        payload = cast(dict[str, object], data.get("payload", {}))

        metadata = MessageMetadata(
            message_type=str(raw_metadata.get("message_type", message_type.__name__)),
            message_id=UUID(str(raw_metadata["message_id"])),
            created_at=datetime.fromisoformat(str(raw_metadata["created_at"])),
            causation_id=UUID(str(raw_metadata["causation_id"])),
            correlation_id=UUID(str(raw_metadata["correlation_id"])),
        )

        return message_type.from_payload_fields(payload, metadata)
