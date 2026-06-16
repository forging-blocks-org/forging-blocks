# Clean Architecture Reference

---

## Quick summary

This page provides a **visual reference** for Clean Architecture layering as it relates to ForgingBlocks concepts.

The diagram shows the four concentric layers:
- **Enterprise Business Rules** (innermost) — Domain (Entities, Value Objects)
- **Application Business Rules** — Application (Use Cases, Handlers)
- **Interface Adapters** — Presentation, Gateways, Controllers
- **Frameworks & Drivers** (outermost) — Infrastructure (DB, Web, External APIs)

Dependencies point inward toward the core.

---

```mermaid
