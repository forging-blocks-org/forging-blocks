# Ports

Foundational Protocol Interfaces.

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

::: building_blocks.foundation.ports
    options:
      show_source: true
      show_root_heading: true
