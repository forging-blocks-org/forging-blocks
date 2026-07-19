"""Next-handler type alias for the middleware pipeline.

``NextHandler`` represents the callable that each middleware delegates
to after performing its own processing. It accepts a request of type
*RequestType* and returns an awaitable that resolves to *ResponseType*.
"""

from collections.abc import Awaitable, Callable

type NextHandler[RequestType, ResponseType] = Callable[[RequestType], Awaitable[ResponseType]]
