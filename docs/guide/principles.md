# Architectural Principles 🧭

**BuildingBlocks** is grounded in timeless software design principles that make systems robust, adaptable, and maintainable.

---

## 🧩 1. Separation of Concerns

Each layer in the architecture has a distinct purpose:
- **Foundation** — core abstractions, no dependencies.
- **Domain** — pure business rules.
- **Application** — orchestration and coordination logic.
- **Infrastructure** — external integrations and persistence.
- **Presentation** — entry points and delivery mechanisms.

This separation avoids coupling between technical and business concerns.

---

## 🧱 2. Dependency Inversion Principle (DIP)

High-level modules (domain, application) define **interfaces (Ports)**.
Low-level modules (infrastructure, presentation) implement those interfaces.

> “Depend on abstractions, not on concretions.” — Robert C. Martin

---

## 🔄 3. Explicit Boundaries

Every dependency is made explicit through **ports** or **contracts**.
You always know what a layer depends on — there are no hidden side effects.

---

## 🧠 4. Immutability and Safety

Entities and Value Objects are **immutable by default**, ensuring that business rules cannot be violated through uncontrolled mutations.

---

## ⚙️ 5. Composability

Everything in BuildingBlocks can be combined like LEGO pieces:
each class, protocol, and helper is small, explicit, and self-contained.

---

## 🧪 6. Testability

Because boundaries are explicit, layers can be **tested in isolation**.
Mocking or substituting ports becomes trivial.

---

## 🏗️ 7. Framework Independence

BuildingBlocks does not force you into a specific runtime or web framework.
You can use it with **FastAPI**, **Django**, **Flask**, **Click**, or even plain scripts — the design remains consistent.

---

## ✅ Summary

BuildingBlocks promotes **intentional design**:
- Each boundary is explicit.
- Each dependency is visible.
- Each decision is reversible.
