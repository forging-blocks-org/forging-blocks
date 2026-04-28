# Domain Blocks

The **domain blocks** is the heart of your business logic.
It is completely independent of frameworks, databases, and other technical concerns.
This blocks models your problem space using core DDD patterns: **Entities, Value Objects, Domain Events, Aggregates, Repositories, and Domain Services**.

---

## 📁 Directory Structure

```
domain/
├── aggregate_root.py            # Base class for aggregate roots
├── entity.py                    # Base class for entities with identity
├── value_object.py              # Base class for value objects (immutables)
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
- **Queries:** Requests for queries (query, not result).
- All are defined in the **Foundation** block as reusable message abstractions.

---

## 🧩 How to Use

1. **Define Entities and Value Objects**
   Extend `Entity` and `ValueObject` to model your business concepts.

   ```python
   from forging_blocks.domain.entity import Entity
   from buidling_blocks.domain.value_object import ValueObject
   2. **Model Aggregates**
      Use `AggregateRoot` for your aggregate boundaries.

   3. **Raise Domain Events**
      Create subclasses of `Event` and use them to communicate important business changes.

   4. **Use Domain Commands and Queries**
       Import from `forging_blocks.foundation.messages` for intent and data retrieval.

   ---

## 🛡️ Testing Guidelines

- Use AAA (Arrange, Act, Assert) pattern.
- Name test classes as `Test<ClassName>`.
- Name test methods as `test_<method>_when_<scenario>_then_<result>`.
- One action (Act) per test.
- Use mocks for outbound ports (repositories, etc.).
- Avoid mocks for pure domain logic.

   ---

## 🧑‍💻 Extending the Domain Blocks

- **Add new entities or value objects** as your blocks grows.
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
