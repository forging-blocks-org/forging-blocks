# Domain Layer 🧠

The **domain layer** is the heart of your business logic.
It is completely independent of frameworks, databases, and other technical concerns.
This layer models your problem space using core DDD patterns: **Entities, Value Objects, Domain Events, Aggregates, Repositories, and Domain Services**.

---

## 📁 Directory Structure

```
domain/
├── aggregate_root.py            # Base class for aggregate roots
├── entity.py                    # Base class for entities with identity
├── value_object.py              # Base class for value objects (immutables)
├── messages/
│   ├── message.py               # Base class for messages (commands/events/queries/any message-like)
│   ├── query.py                 # Base class for domain queries
│   ├── command.py               # Base class for domain commands
│   └── event.py                 # Base class for domain events
└── README.md                    # This documentation
```

---

## ✨ Core Concepts

### 1. **Entities**
- Objects defined by their unique identity and encapsulated logic.
- Inherit from `Entity`.

### 2. **Value Objects**
- Immutable, equality-by-value.
- Inherit from `ValueObject`.

### 3. **Aggregate Roots**
- Entities that control a cluster of domain objects and enforce invariants.
- Inherit from `AggregateRoot`.

### 4. **Domain Commands, Events & Queries**
- **Events:** Things that have happened (immutable, recordable).
- **Commands:** Requests for actions (intent, not result).
- **Queriies:** Requests for queries (query, not result).
- All inherit from `Message` (specialized as `Command`, `Event` or `Query`).

---

## 🧩 How to Use

1. **Define Entities and Value Objects**
   Extend `Entity`, `DraftEntity` and `ValueObject` to model your business concepts.

   ```python
   from building_blocks.domain.entity import Entity
   from buidling_blocks.domain.value_object import ValueObject


   class UserId(ValueObject[str]):
       def __init__(self, id: str):
           self._value = id

        @property
        def value(self) -> str:
            return self._value

        @property
        def _equality_components(self) -> tuple:
            return (self._value,)

   class UserEmail(ValueObject[str]):
       def __init__(self, email: str):
           self._value = value

    @property
    def value(self) -> str:
        return self._value

   @property
    def _equality_components(self) -> tuple:
        return (self._value,)


   class User(Entity):
       def __init__(self, user_id: str, email: UserEmail):
           super().__init__(user_id)
           self._email = email
   ```

2. **Model Aggregates**
   Use `AggregateRoot` for your aggregate boundaries.

3. **Raise Domain Events**
   Create subclasses of `Event` and use them to communicate important business changes.

4. ** Rause Domain Commands and Queries**
    Create subclasses of `Command` and `Query` for intent and data retrieval.

---

## 🛡️ Testing Guidelines

- Use AAA (Arrange, Act, Assert) pattern.
- Name test classes as `Test<ClassName>`.
- Name test methods as `test_<method>_when_<scenario>_then_<result>`.
- One action (Act) per test.
- Use mocks for outbound ports (repositories, etc.).
- Avoid mocks for pure domain logic.

---

## 🧑‍💻 Extending the Domain Layer

- **Add new entities or value objects** as your domain grows.
- **Add outbound ports** for new persistence or integration needs.
- **Add domain services** for complex business rules.
- **Never** import infrastructure, application, or framework code here!

---

## 🏗️ Why This Matters

- **Independence:** Domain logic stays pure and reusable.
- **Testability:** Easy, fast, isolated tests.
- **Maintainability:** Clear separation of business rules from technical detail.

---
**For more examples and full documentation, see the project root [README](../../README.md) or the `/docs` directory.**
