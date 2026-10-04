"""Structural protocol for decorated message classes."""

from typing import Protocol, Self, runtime_checkable

from forging_blocks.domain.messages.message import MessageMetadata


@runtime_checkable
class PatchedMessage(Protocol):
    """Structural type describing a message class after decorator patching.

    This protocol allows pyright to verify that the patched attributes exist
    and have the correct signatures, replacing attribute assignment suppressions
    with a type-safe cast boundary.
    """

    @classmethod
    def from_payload_fields(
        cls,
        data: dict[str, object],
        metadata: MessageMetadata,
    ) -> Self: ...

    def get_payload_fields(self) -> dict[str, object]: ...
