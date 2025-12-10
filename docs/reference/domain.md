
# 🧩 Domain Layer

The **Domain Layer** defines your system’s *core meaning* — its rules, invariants, identity model, and ubiquitous language.
In ForgingBlocks, the domain is intentionally **pure**, **framework‑agnostic**, and **behavior‑centric**.

It models **what the system *is***, not *how* it interacts with databases, APIs, or frameworks.

---

## 🧠 Purpose

The domain layer expresses:

- **Entities** — identity-based concepts
- **Value Objects** — immutable concepts defined by value
- **Aggregate Roots** — consistency boundaries with event recording
- **Domain Messages** — Commands, Events, Queries
- **Domain Errors** — guards for invariants and misuse

Everything here is **side‑effect free** and **does not depend** on infrastructure, presentation, or application layers.

---

## 📁 Directory Structure

```
domain/
├── entity.py
├── value_object.py
├── aggregate_root.py
├── errors/
│   ├── entity_id_none_error.py
│   └── draft_entity_is_not_hashable_error.py
└── messages/
    ├── message.py
    ├── command.py
    ├── event.py
    └── query.py
```

---

# 🧩 Core Building Blocks

## 🪪 1. Entities

Entities are defined by **identity**, not attributes.

- Once set, identity is **immutable**
- Draft entities (`id=None`) are **not hashable**
- Equality is based on the entity’s ID

Example:

```python
class User(Entity[UUID]):
    def __init__(self, user_id: UUID, email: Email):
        super().__init__(user_id)
        self._email = email
```

Behind the scenes, the `Entity` implementation enforces:

- freezing of `_id`
- defensive equality
- draft protection

---

## 🧱 2. Value Objects

A Value Object:

- is **immutable after initialization**
- is compared by **value**
- is hashable (based on its equality components)

Example:

```python
class Email(ValueObject[str]):
    def __init__(self, value: str):
        super().__init__()
        if "@" not in value:
            raise ValueError("Invalid email")
        self._value = value
        self._freeze()

    @property
    def value(self): return self._value
    def _equality_components(self): return (self._value,)
```

---

## 🏛️ 3. Aggregate Roots

Aggregates enforce consistency and record events.

Key features:

- maintain an `AggregateVersion` for optimistic locking
- record events through `record_event`
- expose events through `collect_events()`, which also increments the version

Example:

```python
class Order(AggregateRoot[UUID]):
    def add_item(self, item: OrderItem):
        self._items.append(item)
        self.record_event(OrderItemAdded(...))
```

---

## ✉️ 4. Domain Messages

Messages are immutable value objects used to express:

- **Commands** — intent to change state
- **Events** — facts about what happened
- **Queries** — requests for information

All messages:

- inherit from `Message`
- include automatic `MessageMetadata`
- define a `_payload` part describing domain information

Example Event:

```python
class OrderCreated(Event):
    @property
    def _payload(self):
        return {"order_id": self._order_id}
```

---

## ⚠️ 5. Domain Errors

The domain protects its invariants using explicit domain‑level errors:

- `EntityIdNoneError` — ID must never be None for persisted entities
- `DraftEntityIsNotHashableError` — prevents hashing unpersisted entities

These errors ensure correctness inside the domain boundary.

---

# 🔗 Cross‑Layer Interaction

```
Application → Domain
Domain ↛ Application
Domain ↛ Infrastructure
```

The domain layer is the **center** — everything points *toward* it, but it points to nothing outside itself.

---

# 📝 Summary

| Concept | Responsibility |
|--------|----------------|
| **Entity** | Identity + behavior |
| **Value Object** | Immutable domain concept |
| **AggregateRoot** | Boundary + event recording + versioning |
| **Command** | Intent |
| **Event** | Fact |
| **Query** | Retrieval request |
| **Errors** | Enforce invariants |

---

Forge your domain with clarity, purity, and intention.
This layer is the *truth* of your system.
