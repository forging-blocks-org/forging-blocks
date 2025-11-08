# Reference 📖

The **Reference** section describes each package in **BuildingBlocks** — what it contains, what it depends on, and how it fits into the larger architecture.

---

## 🧩 Package Overview

| Package | Description |
|--------|--------------|
| **Foundation** | Core abstractions (`Result`, `Port`, `Mapper`) shared by all layers |
| **Domain** | Domain layer. Contains business rules and ubiquitous language |
| **Application** | Application layer. Contains ports(inbound or outbound) and services that implement the application logic. |
| **Infrastructure** | Infrastructure layer. Adapters for external systems |
| **Presentation** | Presentation layer. Entry points (API, CLI, event consumers) |

---

## 📚 Contents

- [Foundation](foundation.md)
- [Domain](domain.md)
- [Application](application.md)
- [Infrastructure](infrastructure.md)
- [Presentation](presentation.md)
- [Example Tests](example_tests.md)
