"""Message codec ABC for encoding/decoding foundation messages."""

from abc import abstractmethod

from forging_blocks.foundation import FinalABCMeta, runtime_final


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

    @runtime_final
    def encode(self, message: M) -> Raw:
        """Encode *message* to its raw representation.

        Delegates to :meth:`_to_data` which subclasses must implement.
        """
        return self._to_data(message)

    @runtime_final
    def decode(self, data: Raw, message_type: type[M]) -> M:
        """Decode *data* back into a message of *message_type*.

        Delegates to :meth:`_from_data` which subclasses must implement.
        """
        return self._from_data(data, message_type)

    @abstractmethod
    def _to_data(self, message: M) -> Raw:
        """Convert *message* to its raw representation.

        Subclasses implement the serialization logic.

        Args:
            message: The message instance to encode.

        Returns:
            The raw representation of the message.
        """
        ...

    @abstractmethod
    def _from_data(self, data: Raw, message_type: type[M]) -> M:
        """Reconstruct a message from its raw representation.

        Subclasses implement the deserialization logic.

        Args:
            data: The raw data to decode.
            message_type: The target message class (used to dispatch).

        Returns:
            A new message instance of type *message_type*.
        """
        ...
