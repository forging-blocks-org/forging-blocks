"""Foundational Protocol Interfaces.

Defines general-purpose protocol interfaces for **type-annotated contracts**.
These are "super interfaces" (marker protocols) that you extend to create
your own interface definitions with excellent IDE support and architectural
flexibility. They impose no framework or layout requirements.

WHAT ARE THESE PROTOCOLS?
-------------------------

.. code-block:: text

    ┌─────────────────────────────────────────────────────────────────────────────┐
    │  WHAT ARE THESE PROTOCOLS?                                                  │
    ├─────────────────────────────────────────────────────────────────────────────┤
    │                                                                             │
    │  Port, InboundPort, and OutboundPort are generic Protocol classes that      │
    │  serve as foundations for your own interface definitions.                   │
    │                                                                             │
    │  ✓ They Provide:                                                            │
    │    • Generic type parameters (InputType, OutputType)                        │
    │    • Structural typing support (PEP 544)                                    │
    │    • Consistent naming conventions                                          │
    │    • IDE autocomplete and static analysis                                   │
    │    • Zero dependencies or framework requirements                            │
    │                                                                             │
    │  ✗ They DON'T Provide:                                                      │
    │    • Any predefined methods                                                 │
    │    • Architectural constraints or patterns                                  │
    │    • Implementation requirements                                            │
    │    • Framework or library dependencies                                      │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘

QUICK START: THE THREE-STEP PATTERN
-----------------------------------

Step 1: Define Your Protocol (extend + add methods)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from building_blocks.foundation.ports import OutboundPort

    class UserRepository(OutboundPort[UserID, User]):
        # Repository interface for user persistence.

        def find_by_id(self, id: UserID) -> User | None:
            # Retrieve a user by their unique ID.
            ...

        def find_by_email(self, email: str) -> User | None:
            # Retrieve a user by their email address.
            ...

        def save(self, user: User) -> None:
            # Persist a user (insert or update).
            ...

        def delete(self, id: UserID) -> bool:
            # Remove a user. Returns True if user existed.
            ...

Step 2: Implement It (as many times as needed)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Production: PostgreSQL implementation
    class PostgresUserRepository:
        def __init__(self, connection_pool):
            self.db = connection_pool

        def find_by_id(self, id: UserID) -> User | None:
            row = self.db.query_one("SELECT * FROM users WHERE id = $1", id)
            return User.from_row(row) if row else None

        def find_by_email(self, email: str) -> User | None:
            row = self.db.query_one("SELECT * FROM users WHERE email = $1", email)
            return User.from_row(row) if row else None

        def save(self, user: User) -> None:
            self.db.execute(
                (
                    "INSERT INTO users (id, email, name) "
                    "VALUES ($1, $2, $3) "
                    "ON CONFLICT (id) DO UPDATE SET email=$2, name=$3"
                ),
                user.id, user.email, user.name
            )

        def delete(self, id: UserID) -> bool:
            result = self.db.execute("DELETE FROM users WHERE id = $1", id)
            return result.rowcount > 0

    # Testing: In-memory fake implementation
    class InMemoryUserRepository:
        def __init__(self):
            self._users: dict[UserID, User] = {}
            self._by_email: dict[str, UserID] = {}

        def find_by_id(self, id: UserID) -> User | None:
            return self._users.get(id)

        def find_by_email(self, email: str) -> User | None:
            user_id = self._by_email.get(email)
            return self._users.get(user_id) if user_id else None

        def save(self, user: User) -> None:
            self._users[user.id] = user
            self._by_email[user.email] = user.id

        def delete(self, id: UserID) -> bool:
            if id in self._users:
                user = self._users.pop(id)
                self._by_email.pop(user.email, None)
                return True
            return False

Step 3: Use Type Hints (swap implementations freely)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def register_new_user(
        repository: UserRepository,  # ← The protocol, not the implementation
        email: str,
        name: str
    ) -> User:
        # Register a new user account.
        existing = repository.find_by_email(email)
        if existing:
            raise ValueError(f"Email {email} is already registered")

        user = User(id=generate_id(), email=email, name=name)
        repository.save(user)
        return user

    # Production: use real database
    db_repo = PostgresUserRepository(db_pool)
    user = register_new_user(db_repo, "alice@example.com", "Alice")

    # Testing: use in-memory fake (fast, no database needed!)
    test_repo = InMemoryUserRepository()
    user = register_new_user(test_repo, "bob@example.com", "Bob")

PROTOCOL HIERARCHY
------------------

.. code-block:: text

    Port[InputType, OutputType]
     │
     ├── InboundPort[InputType, OutputType]  (alias: InputPort)
     │    └─→ For operations that receive and process input
     │        Examples: handlers, processors, validators, executors
     │
     └── OutboundPort[InputType, OutputType] (alias: OutputPort)
          └─→ For operations that interact with external systems
              Examples: repositories, caches, APIs, message brokers

    All three are marker protocols — they define no methods.
    You extend them and add your own method signatures.

WHY USE THESE PROTOCOLS?
------------------------

Type Annotations (static analysis at dev time)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def process(repo: UserRepository, id: UserID):
        user = repo.find_by_id(id)    # static analyzers infer the return type
        # user.invalid_method()       # analyzers flag this as an error

IDE Support
~~~~~~~~~~~

Modern IDEs provide autocomplete, jump-to-definition, and inline documentation
for protocol-based interfaces.

.. code-block:: python

    repo.find_  # ← IDE shows: find_by_id(), find_by_email()

Testability
~~~~~~~~~~~

Swap real implementations with test doubles (fakes, mocks, stubs) without
changing your business logic.

.. code-block:: python

    # Production
    service = UserService(PostgresUserRepository(db))

    # Testing
    service = UserService(InMemoryUserRepository())

Flexibility
~~~~~~~~~~~

Multiple implementations of the same interface; change implementations without
modifying callers.

Documentation
~~~~~~~~~~~~~

Protocols make contracts explicit and self-documenting through type hints.
The interface defines what's expected, not how it's implemented.

Independence
~~~~~~~~~~~~

No framework dependencies. No architectural constraints. Works in any Python
application structure.

TYPE PARAMETERS EXPLAINED
-------------------------

InputType: The data type your operations work with
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Often represents:

- IDs for lookup operations (UserID, ProductID, OrderID)
- Query objects for search operations (SearchQuery, Filter)
- Data to be processed or validated (FormData, Document)
- Keys for cache operations (CacheKey, str)
- Commands or requests (CreateUserCommand, PaymentRequest)

Examples:
- Repository[UserID, User]           # Input: ID
- Cache[str, bytes]                  # Input: cache key
- Processor[RawData, ProcessedData]  # Input: data to process

OutputType: The data type your operations return
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Often represents:

- Entities or aggregates (User, Product, Order)
- Result objects (SearchResult, ValidationResult, PaymentResult)
- Optional data (User | None)
- Collections (list[Product], dict[str, Any])
- Status or confirmation (bool, None)

Examples:
- Repository[UserID, User]           # Output: User entity
- Cache[str, bytes]                  # Output: cached bytes
- Validator[Data, list[Error]]       # Output: list of errors

STRUCTURAL TYPING (PEP 544)
---------------------------

Implementations don't need to explicitly inherit from your protocols. They only
need to implement the required methods (structural subtyping).

.. code-block:: python

    class MyRepository:  # No inheritance needed
        def find_by_id(self, id: UserID) -> User | None:
            return self._users.get(id)

        def save(self, user: User) -> None:
            self._users[user.id] = user

    repo: UserRepository = MyRepository()  # static analyzers accept this

You can also inherit explicitly (optional):

.. code-block:: python

    class MyRepository(UserRepository):  # Explicit inheritance
        def find_by_id(self, id: UserID) -> User | None:
            return self._users.get(id)

        def save(self, user: User) -> None:
            self._users[user.id] = user

COMMON USAGE PATTERNS
---------------------

Pattern 1: Repository (Data Persistence)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class ProductRepository(OutboundPort[ProductID, Product]):
        def find_by_id(self, id: ProductID) -> Product | None: ...
        def find_by_category(self, category: str) -> list[Product]: ...
        def save(self, product: Product) -> None: ...
        def delete(self, id: ProductID) -> bool: ...

Pattern 2: Cache (Fast Data Access)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class SessionCache(OutboundPort[SessionID, SessionData]):
        async def get(self, id: SessionID) -> SessionData | None: ...
        async def set(self, id: SessionID, data: SessionData, ttl: int) -> None: ...
        async def delete(self, id: SessionID) -> bool: ...

Pattern 3: Use Case / Command Handler (Business Logic)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class CreateOrderUseCase(InboundPort[OrderData, Order]):
        def execute(self, data: OrderData) -> Order: ...
        def validate(self, data: OrderData) -> list[ValidationError]: ...

Pattern 4: Query Handler (Data Retrieval)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class SearchProducts(InboundPort[SearchQuery, SearchResult]):
        async def search(self, query: SearchQuery) -> SearchResult: ...
        async def suggest(self, partial: str) -> list[str]: ...

Pattern 5: External API Client (Third-Party Integration)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class PaymentGateway(OutboundPort[PaymentRequest, PaymentResult]):
        async def charge(self, request: PaymentRequest) -> PaymentResult: ...
        async def refund(self, transaction_id: str) -> PaymentResult: ...

Pattern 6: Message Broker (Async Communication)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class EventPublisher(OutboundPort[DomainEvent, None]):
        async def publish(self, event: DomainEvent) -> None: ...
        async def publish_batch(self, events: list[DomainEvent]) -> None: ...

Pattern 7: Notification Gateway (Multi-Channel Messaging)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class NotificationSender(OutboundPort[Notification, bool]):
        async def send_email(self, notification: Notification) -> bool: ...
        async def send_sms(self, notification: Notification) -> bool: ...
        async def send_push(self, notification: Notification) -> bool: ...

USAGE IN DIFFERENT ARCHITECTURES
--------------------------------

These protocols are architecture-agnostic and work in any structure:

- Layered Architecture — use ports to define boundaries between layers
- MVC Applications — define contracts between models, views, controllers
- Microservices — define ports for service-to-service communication
- Single-File Scripts — use ports even in simple scripts for testability
- Domain-Driven Design — repositories and domain services as ports
- Hexagonal / Ports-and-Adapters — a natural fit
- Clean Architecture — ports define boundaries and dependencies
- Your Custom Structure — no assumptions

TESTING STRATEGIES
------------------

Strategy 1: In-Memory Fakes (Fast Unit Tests)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Production
    repo = PostgresUserRepository(db_pool)

    # Testing (no database, instant)
    repo = InMemoryUserRepository()

    # Test runs in microseconds
    user = User(id="123", email="test@example.com")
    repo.save(user)
    assert repo.find_by_id("123") == user

Strategy 2: Mock Objects (Verify Interactions)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from unittest.mock import Mock

    mock_repo = Mock(spec=UserRepository)
    mock_repo.find_by_id.return_value = User(...)

    service = UserService(mock_repo)
    service.get_user("123")

    mock_repo.find_by_id.assert_called_once_with("123")

Strategy 3: Test Doubles with State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class SpyRepository:
        def __init__(self):
            self.saved_users = []
            self.deleted_ids = []

        def save(self, user: User) -> None:
            self.saved_users.append(user)

        def delete(self, id: UserID) -> bool:
            self.deleted_ids.append(id)
            return True

    # Verify behavior
    spy = SpyRepository()
    service.register_user(spy, "alice@example.com", "Alice")
    assert len(spy.saved_users) == 1
    assert spy.saved_users[0].email == "alice@example.com"

PROTOCOL DEFINITIONS
--------------------

See Also:
- PEP 544 — Protocols: Structural subtyping (static duck typing)
- typing.Protocol — Python's Protocol implementation
"""

# pyright: reportInvalidTypeVarUse=false
from typing import Generic, Protocol, TypeVar

InputType = TypeVar("InputType", contravariant=True)
OutputType = TypeVar("OutputType", covariant=True)


class Port(Protocol, Generic[InputType, OutputType]):
    """Base protocol for defining interface contracts.

    Port is a generic Protocol that serves as the foundation for interface
    declarations. It provides type parameters (InputType, OutputType) and
    defines no methods — it's a marker protocol that you extend to create your
    own specific interfaces.

    WHEN TO USE
    -----------
    - Use ``Port`` directly when the Inbound/Outbound naming does not fit.
    - Use ``InboundPort`` for operations that receive/process input.
    - Use ``OutboundPort`` for interfaces to external systems.

    TYPE PARAMETERS
    ---------------
    - ``InputType``:  the type of data accepted by operations on this interface
    - ``OutputType``: the type of data returned by operations on this interface

    DESIGN NOTES
    ------------
    - Marker protocol: derived protocols add whatever methods make sense.
    - Structural typing (PEP 544): implementations need not inherit explicitly.
    - Common ancestor for the port hierarchy.

    EXAMPLE: DATA TRANSFORMER
    -------------------------

    .. code-block:: python

        from building_blocks.foundation import Port

        class DataTransformer(Port[SourceFormat, TargetFormat]):
            # Transform data from one format to another.
            def transform(self, source: SourceFormat) -> TargetFormat: ...
            def can_transform(self, source: SourceFormat) -> bool: ...
            def get_errors(self, source: SourceFormat) -> list[str]: ...

        class JSONToXMLTransformer:
            def transform(self, source: dict) -> str:
                import xml.etree.ElementTree as ET
                root = ET.Element("root")
                for key, value in source.items():
                    child = ET.SubElement(root, key)
                    child.text = str(value)
                return ET.tostring(root, encoding="unicode")

            def can_transform(self, source: dict) -> bool:
                return isinstance(source, dict)

            def get_errors(self, source: dict) -> list[str]:
                if not isinstance(source, dict):
                    return ["Source must be a dictionary"]
                return []

        def convert_data(transformer: DataTransformer[dict, str], data: dict) -> str:
            if not transformer.can_transform(data):
                errors = transformer.get_errors(data)
                raise ValueError(f"Cannot transform: {errors}")
            return transformer.transform(data)
    """

    ...

    def __port_variance__(self, __x: InputType) -> OutputType:
        """Private helper to make type variance explicit (for static checkers)."""
        ...


class InboundPort(Port[InputType, OutputType], Protocol):
    """Protocol foundation for defining inbound operation interfaces.

    ``InboundPort`` is intended for operations that receive input and produce
    output (e.g., handlers, processors, validators, use cases).

    COMMON USE CASES
    ----------------
    - Request handlers (HTTP, GraphQL, gRPC)
    - Command executors (CQRS commands)
    - Query processors (CQRS queries)
    - Data validators and processors
    - Use cases / application services
    - Event handlers and workflow executors

    USAGE PATTERN
    -------------
    1. Extend ``InboundPort`` and define your methods.
    2. Implement with one or more concrete classes.
    3. Use as type hints in your functions.
    4. Swap implementations as needed (production, testing, etc.).

    EXAMPLE: COMMAND HANDLER
    ------------------------

    .. code-block:: python

        class CreateUserCommand(InboundPort[UserRegistrationData, User]):
            def execute(self, data: UserRegistrationData) -> User: ...
            def validate(self, data: UserRegistrationData) -> list[ValidationError]: ...

        class CreateUserCommandHandler:
            def __init__(self, user_repo: UserRepository, email_service: EmailService):
                self.user_repo = user_repo
                self.email_service = email_service

            def execute(self, data: UserRegistrationData) -> User:
                errors = self.validate(data)
                if errors:
                    raise ValidationError(errors)

                if self.user_repo.find_by_email(data.email):
                    raise ValueError("Email already registered")

                user = User(
                    id=generate_id(),
                    email=data.email,
                    name=data.name,
                    created_at=datetime.now(),
                )

                self.user_repo.save(user)
                self.email_service.send_welcome(user.email, user.name)
                return user

            def validate(self, data: UserRegistrationData) -> list[ValidationError]:
                errors: list[ValidationError] = []
                if not data.email or "@" not in data.email:
                    errors.append(ValidationError("Invalid email"))
                if not data.name or len(data.name) < 2:
                    errors.append(ValidationError("Name too short"))
                if len(data.password) < 8:
                    errors.append(ValidationError("Password too weak"))
                return errors
    """

    ...


class OutboundPort(Port[InputType, OutputType], Protocol):
    """Protocol foundation for defining outbound operation interfaces.

    ``OutboundPort`` is intended for operations that interact with external
    systems, resources, or services (e.g., repositories, caches, APIs,
    message brokers, storage, search).

    COMMON USE CASES
    ----------------
    - Repositories (data persistence)
    - Cache systems (fast data access)
    - Message brokers (async communication)
    - External API clients (third-party services)
    - Email/SMS gateways (notifications)
    - Search engines (full-text search)
    - File storage (object storage, S3)
    - Event publishers (event-driven systems)
    - Logging systems (centralized logging)

    USAGE PATTERN
    -------------
    1. Extend ``OutboundPort`` and define your methods.
    2. Implement for different backends (SQL, NoSQL, in-memory, etc.).
    3. Use as type hints in your business logic.
    4. Swap implementations based on environment or requirements.

    EXAMPLE: REPOSITORY PATTERN
    ---------------------------

    .. code-block:: python

        class OrderRepository(OutboundPort[OrderID, Order]):
            def find_by_id(self, id: OrderID) -> Order | None: ...
            def find_by_customer(self, customer_id: CustomerID) -> list[Order]: ...
            def find_pending(self) -> list[Order]: ...
            def save(self, order: Order) -> None: ...
            def delete(self, id: OrderID) -> bool: ...

        class PostgresOrderRepository:
            def __init__(self, connection_pool):
                self.db = connection_pool

            def find_by_id(self, id: OrderID) -> Order | None:
                row = self.db.query_one(
                    "SELECT id, customer_id, total, status, created_at FROM orders WHERE id = $1",
                    id,
                )
                return Order.from_row(row) if row else None

            def find_by_customer(self, customer_id: CustomerID) -> list[Order]:
                rows = self.db.query(
                    (
                        "SELECT id, customer_id, total, status, created_at "
                        "FROM orders WHERE customer_id = $1 "
                        "ORDER BY created_at DESC"
                    ),
                    customer_id,
                )
                return [Order.from_row(row) for row in rows]

            def find_pending(self) -> list[Order]:
                rows = self.db.query(
                    (
                        "SELECT id, customer_id, total, status, created_at "
                        "FROM orders WHERE status = 'pending' "
                        "ORDER BY created_at ASC"
                    )
                )
                return [Order.from_row(row) for row in rows]

            def save(self, order: Order) -> None:
                self.db.execute(
                    (
                        "INSERT INTO orders (id, customer_id, total, status, created_at) "
                        "VALUES ($1, $2, $3, $4, $5) "
                        "ON CONFLICT (id) DO UPDATE "
                        "SET customer_id=$2, total=$3, status=$4, created_at=$5"
                    ),
                    order.id,
                    order.customer_id,
                    order.total,
                    order.status,
                    order.created_at,
                )

            def delete(self, id: OrderID) -> bool:
                result = self.db.execute("DELETE FROM orders WHERE id = $1", id)
                return result.rowcount > 0

        def complete_order(repository: OrderRepository, order_id: OrderID) -> Order:
            # Mark an order as completed.
            order = repository.find_by_id(order_id)
            if not order:
                raise OrderNotFound(f"Order {order_id} not found")
            if order.status != "pending":
                raise InvalidOperation("Only pending orders can be completed")

            order.status = "completed"
            order.completed_at = datetime.now()
            repository.save(order)
            return order
    """

    ...


InputPort = InboundPort
OutputPort = OutboundPort
