
# 🧭 Domain Reference Index

This section documents the **Domain Layer** primitives of ForgingBlocks — the tools you use to model your business rules and invariant‑driven behavior.

---

## 📚 Contents

### 🔹 Modeling
- [Entities](entity.md)
- [Value Objects](value_object.md)
- [Aggregate Roots](aggregate_root.md)

### 🔹 Messaging
- [Message](message.md)
- [Command](command.md)
- [Event](event.md)
- [Query](query.md)

### 🔹 Errors
- [EntityIdNoneError](entity_id_none_error.md)
- [DraftEntityIsNotHashableError](draft_entity_is_not_hashable_error.md)

---

## 🧠 Philosophy

The Domain Layer represents the **pure core** of the system.
It expresses the rules and meaning of the business model using behavior‑centric building blocks.

ForgingBlocks provides strict, defensive implementations to reinforce:

- identity immutability
- value object immutability
- aggregate consistency
- message uniqueness
- event ordering
- domain invariant enforcement

---

## 🧩 How to Use This Reference

Use this index as a map:

- Start with **Entities & Value Objects** to model domain concepts.
- Use **Aggregates** to define boundaries and event recording.
- Use **Commands / Events / Queries** to express intent and facts.
- Use **Domain Errors** to enforce correctness.

Each page in this section provides:
- explanation
- guidelines
- examples
- usage notes

---

Build domains with intention.
Structure follows meaning — and meaning lives here.
