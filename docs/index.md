# BuildingBlocks 🧩

A composable **architecture toolkit** for building clean, testable, and maintainable Python applications.

---

## 🧠 Philosophy

Most Python codebases start small — and soon collapse under unclear boundaries.
**Building Blocks** helps you *design your system with intent* by providing
**abstractions and interfaces** that can compose into any architectural style.

It’s not a framework.
It’s a **toolkit of base contracts and abstract classes** — simple, type-safe, framework-agnostic.

---

## 🧩 What It Offers

### Foundation

Core interfaces, protocols, and helpers that form the language of composition:

- `Result`, `Ok`, `Err` for explicit success/failure
- `Mapper` and `ResultMapper` for safe transformations
- `Port`, `InboundPort`, `OutboundPort` for boundary design

### Domain

Base classes for rich domain modeling:

- `Entity`
- `ValueObject`
- `AggregateRoot`

### Application

Base protocols for inbound ports:
- `UseCase`
- `MessageHandler`
- `CommandHandler`
- `EventHandler`
- `QueryHandler`

Base protocols, and base implementations, for outbound ports:
- `CommandSender`
- `EventPublisher`
- `MessageBus`
- `Notifier`
- `QueryFetcher`
- `Repository`
- `UnitOfWork`

---

## ⚙️ Works With Any Style

| Style | How to Use Building Blocks |
|--------|-----------------------------|
| **One-file application** | Use `Port` or `InboundPort` and `OutboundPort` as adapters. |
| **Microservices** | Define service boundaries with `InboundPort` and `OutboundPort`. |
| **MVC** | Use `InboundPort` for Controllers and `OutboundPort` for Models. |
| **MVVM** | Use `InboundPort` for ViewModels and `OutboundPort` for Models. |
| **MVP** | Use `InboundPort` for Presenters and `OutboundPort` for Models. |
| **Service-Oriented Architecture (SOA)** | Define service contracts with `InboundPort` and `OutboundPort`. |
| **Domain-Driven Design (DDD)** | Use `Entity`, `ValueObject`, `AggregateRoot`, and `Repository` for rich modeling. |
| **Microkernel Architecture** | Use `InboundPort` and `OutboundPort` to define core and plugin interactions. |
| **Service Layer Architecture** | Use `UseCase` and `Repository` to define service boundaries. |
| **Client-Server Architecture** | Use `InboundPort` for server-side handlers and `OutboundPort` for client requests. |
| **Peer-to-Peer Architecture** | Use `InboundPort` and `OutboundPort` for peer communication protocols. |
| **Message-Driven Architecture** | Use `MessageHandler`, `CommandHandler`, `EventHandler`, and `QueryHandler` for message processing. |
| **Hexagonal Architecture** | Use `InboundPort` and `OutboundPort` for define your specific `Protocol` or interface.|
| **Clean Architecture** | Define your use cases and boundaries explicitly based in the provided ports. |
| **Layered Architecture** | Use provided ports to separate persistence, domain, and service logic. |
| **Event-Driven or CQRS** | Combine `Result`, `Event`, `Command`, `Query` and other foundation definitions. |

---

## 🚀 Get Started

```bash
poetry add building-blocks
```

or see the [Getting Started Guide](guide/getting-started.md).

---

## 🧭 Explore the Toolkit

- [Architecture Guide](guide/architecture.md)
- [API Reference](reference/index.md)

Examples are being migrated to a dedicated repository — link coming soon.

---

## 🧑‍💻 Community & Credits

**Building Blocks** is maintained by the [Building Blocks Organization](https://github.com/building-blocks-org),
originally created by [Glauber Brennon](https://github.com/gbrennon).

MIT License — contributions welcome ❤️
