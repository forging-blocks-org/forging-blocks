"""Authorization context bundled for a single authorization decision."""

from collections.abc import Hashable

from forging_blocks.domain.value_object import ValueObject


class AuthorizationContext(ValueObject[tuple[Hashable, ...]]):
    """Bundles the information needed for a single authorization decision.

    Args:
        user_id: The unique identifier of the user requesting access.
        roles: Roles assigned to the user (e.g. ``("admin", "editor")``).
        resource_id: Optional identifier of the resource being accessed.
        resource_type: Optional discriminator for the resource kind
            (e.g. ``"document"``, ``"project"``).
        action: Optional name of the action being performed
            (e.g. ``"publish"``, ``"archive"``).
        metadata: Arbitrary key-value pairs that checkers may inspect.

    """

    __slots__ = (
        "_user_id",
        "_roles",
        "_resource_id",
        "_resource_type",
        "_action",
        "_metadata",
    )

    def __init__(
        self,
        user_id: str,
        *,
        roles: tuple[str, ...] = (),
        resource_id: str | None = None,
        resource_type: str | None = None,
        action: str | None = None,
        metadata: tuple[tuple[str, Hashable], ...] = (),
    ) -> None:
        super().__init__()
        self._user_id = user_id
        self._roles = roles
        self._resource_id = resource_id
        self._resource_type = resource_type
        self._action = action
        self._metadata = metadata

    @property
    def user_id(self) -> str:
        """The unique identifier of the user requesting access."""
        return self._user_id

    @property
    def roles(self) -> tuple[str, ...]:
        """Roles assigned to the user (e.g. ``("admin", "editor")``)."""
        return self._roles

    @property
    def resource_id(self) -> str | None:
        """Optional identifier of the resource being accessed."""
        return self._resource_id

    @property
    def resource_type(self) -> str | None:
        """Optional discriminator for the resource kind."""
        return self._resource_type

    @property
    def action(self) -> str | None:
        """Optional name of the action being performed."""
        return self._action

    @property
    def metadata(self) -> tuple[tuple[str, Hashable], ...]:
        """Arbitrary key-value pairs that checkers may inspect."""
        return self._metadata

    @property
    def value(self) -> tuple[Hashable, ...]:
        """Composite value: all fields as a tuple."""
        return (
            self._user_id,
            self._roles,
            self._resource_id,
            self._resource_type,
            self._action,
            self._metadata,
        )
