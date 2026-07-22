"""Protocol for translating transport-level requests into application input."""

from typing import Protocol


class RequestAdapter[RawRequest, UseCaseInput](Protocol):
    """Translates a raw transport request into application-layer input.

    Implementations handle transport-specific deserialization (e.g.
    parsing JSON bodies, extracting headers, normalising query
    parameters) and produce a typed use-case input DTO or command.
    """

    def adapt(self, raw: RawRequest) -> UseCaseInput:
        """Convert *raw* transport data into use-case input.

        Args:
            raw: The transport-level request (e.g. an HTTP request
                object, a CLI argv tuple, or a raw dictionary).

        Returns:
            A typed input value suitable for passing to a
            ``UseCasePort.execute`` call.

        """
        ...
