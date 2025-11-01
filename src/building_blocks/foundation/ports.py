"""
This module defines the core abstractions (Ports) that enforce architectural boundaries
between the application core and external systems.

A **Port** represents a *contract* — a protocol that defines how the core communicates
with the outside world, while remaining agnostic to any technical or infrastructural
details.
This enforces the **Dependency Inversion Principle (DIP)**, ensuring that high-level
business logic depends only on abstractions, not concrete implementations.

The module provides three key interfaces:

1. **Port** — The generic root protocol, defining variance-safe type parameters
   (`InputType`, `OutputType`) for all communication boundaries.
2. **InboundPort** — A specialization for *inbound* operations, representing
   entry points into the application core (use cases, command/query handlers).
3. **OutboundPort** — A specialization for *outbound* operations, representing
   dependencies the core relies on (repositories, gateways, external services).

To improve developer ergonomics and maintain parity with Clean Architecture naming,
`InputPort` and `OutputPort` are defined as aliases to `InboundPort` and `OutboundPort`.

Together, these abstractions serve as the foundation of *ports and adapters* (hexagonal)
architecture within the Building Blocks toolkit.
"""

from typing import Generic, Protocol, TypeVar

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class Port(Protocol, Generic[InputType, OutputType]):  # type: ignore[misc]
    """
    A **super interface** (base interface) that serves as a foundation for defining
    communication boundaries (Ports) between the application core and external systems.
    Derived interfaces are free to define their public API.

    This abstraction underpins both **inbound** and **outbound** contracts:

    * **Inbound Ports** — Represent entry points *into* the core.
        - Example: Use Cases, Command Handlers, Query Handlers.
        - Typically define methods like `execute(input: InputType) -> OutputType`.

    * **Outbound Ports** — Represent dependencies the core relies on.
        - Example: Repositories, Message Buses, External APIs.
        - Define their own specialized methods (e.g., `save`, `send_email`, `fetch`).

    ---
    ### Design Goals
    1. Enforce **dependency inversion** — the core depends only on abstractions.
    2. Provide **type safety** and IDE assistance across layers.
    3. Serve as a **common ancestor** for all ports (both inbound and outbound).

    ### Design Intent
    - Define variance-safe type parameters for input and output.
    - Serve as a marker interface for all port types.
    - Enable consistent typing across the application architecture.

    """

    ...


class InboundPort(Port[InputType, OutputType], Protocol):  # type: ignore[misc]
    """
    Represents an **inbound port** — an entry point into the application core.

    Inbound ports define operations that external actors (e.g., controllers,
    message consumers, schedulers) can invoke to drive business logic.

    Examples include:
        - Use Cases
        - Command Handlers
        - Query Handlers

    ---
    ### Design Goals
    1. Expose **business-oriented operations** of the core.
    2. Abstract away technical details of how requests arrive.
    3. Promote **testability** — can be easily mocked or stubbed in tests

    ### Design Intent
    - Define clear entry points for core business logic.
    - Remain agnostic to transport mechanisms (HTTP, messaging, CLI, etc.).
    - Facilitate **separation of concerns** between core logic and delivery mechanisms.
    """

    ...


class OutboundPort(Port[InputType, OutputType], Protocol):  # type: ignore[misc]
    """
    Represents an **outbound port** — a dependency the application core
    relies on to communicate with the external world.

    Outbound ports define *what the core needs* from the external world,
    not *how* it is implemented. They are implemented by adapters in the
    infrastructure layer.

    Examples include:
        - Repositories
        - Message Brokers
        - Email Senders
        - External APIs Client
        - Caching Systems
        - Search Gateways

    ---
    ### Design Intent
    - Express **business-oriented needs** of the core.
    - Remain agnostic to technology (SQL, Redis, Kafka, SMTP, etc.).
    - Promote **replaceability** — any implementation fulfilling the interface
      can be swapped without affecting the core.

    ---
    ### Example

    ```python

    class UserRepository(OutboundPort[UserID, User]):
        async def fetch(self, user_id: UserID) -> User:
            ...

        async def save(self, user: User) -> None:
            ...

    class MessageBroker(OutboundPort[BrokerMessage, None]):
        async def publish(self, message: BrokerMessage) -> None:
            ...

        async def subscribe(self, topic: str) -> AsyncIterator[BrokerMessage]:
            ...

        async def unsubscribe(self, topic: str) -> None:
            ...

        async def acknowledge(self, message: BrokerMessage) -> None:
            ...

        async def reject(self, message: BrokerMessage) -> None:
            ...

        async def purge(self, topic: str) -> None:
            ...

        async def get_stats(self) -> BrokerStats:
            ...

        async def connect(self) -> None:
            ...

        async def disconnect(self) -> None:
            ...

    class EmailSender(OutboundPort[EmailMessage, None]):
        async def send(self, message: EmailMessage) -> None:
            ...

    class ExternalApiClient(OutboundPort[ApiRequest, ApiResponse]):
        async def get(self, request: ApiRequest) -> ApiResponse:
            ...

        async def post(self, request: ApiRequest) -> ApiResponse:
            ...

    class CacheGateway(OutboundPort[CacheKey, CacheValue]):
        async def get(self, key: CacheKey) -> CacheValue:
            ...

        async def set(self, key: CacheKey, value: CacheValue) -> None:
            ...

    class SearchGateway(OutboundPort[SearchQuery, SearchResults]):
        async def search(self, query: SearchQuery) -> SearchResults:
            ...
    ```

    This example illustrates various outbound ports representing dependencies
    the application core might rely on, each defining methods relevant to their
    specific domain.
    """

    ...


InputPort = InboundPort
OutputPort = OutboundPort
