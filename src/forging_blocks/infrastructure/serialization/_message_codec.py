"""Message codec ABC for encoding/decoding foundation messages."""

from abc import abstractmethod

from forging_blocks.foundation import FinalABCMeta


class MessageCodec[M, Raw](metaclass=FinalABCMeta):
    """Abstract codec for encoding and decoding messages.

    A *codec* is a bidirectional transformation between a message
    instance and a raw representation.  Subclasses implement the
    serialization format (dict, bytes, wire protocol, etc.).

    Type Parameters:
        M: The message type this codec handles.
        Raw: The raw representation produced/consumed (e.g., ``dict``,
            ``bytes``, ``str``).
    """

    @abstractmethod
    def encode(self, message: M) -> Raw:
        """Encode *message* to its raw representation.

        Args:
            message: The message instance to encode.

        Returns:
            The raw representation of the message.
        """
        ...

    @abstractmethod
    def decode(self, data: Raw, message_type: type[M]) -> M:
        """Decode *data* back into a message of *message_type*.

        Args:
            data: The raw data to decode.
            message_type: The target message class (used to dispatch).

        Returns:
            A new message instance of type *message_type*.
        """
        ...
