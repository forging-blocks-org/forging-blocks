# Testing Strategy 🧪

Testing in **BuildingBlocks** focuses on **behavior, not framework integration**.
Because each layer is decoupled, tests can target functionality at the right abstraction level.

---

## 🧩 Layer Testing Strategy

| Layer | What to Test | How |
|--------|---------------|----|
| **Foundation** | Result behavior, immutability helpers | Pure unit tests |
| **Domain** | Entities, ValueObjects, DomainEvents | Unit tests (no mocks) |
| **Application** | UseCases, Ports, and orchestration | Unit + Integration (mock outbound ports) |
| **Infrastructure** | Adapters, repositories, event buses | Integration or end-to-end tests |
| **Presentation** | API endpoints, CLI, UI behavior | End-to-end or functional tests |

---

## 🧱 Example Structure

```
tests/
├── foundation/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

---

## 🧠 Principles

1. **Test Behavior, Not Implementation.**
   Validate *what* the code does, not *how* it does it.

2. **Use Ports as Mocks.**
   Mock or fake outbound ports when testing use cases.

3. **Domain Is Sacred.**
   Domain tests should require **no mocking** — they must be pure and deterministic.

---

## ✅ Summary

BuildingBlocks makes testing natural by enforcing clear architectural boundaries.
Each test suite can evolve independently, mirroring your layered structure.
