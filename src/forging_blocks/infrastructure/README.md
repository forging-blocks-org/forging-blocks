# Infrastructure Layer Guidelines 🏗️

This directory provides **generic, reusable infrastructure building blocks**
that implement the outbound ports defined in the application layer.

---

## Available Building Blocks

| Component | Description |
|---|---|
| `InMemoryReadRepository` | In-memory `ReadOnlyRepository` for query-side operations |
| `InMemoryWriteRepository` | In-memory `WriteOnlyRepository` for command-side operations |
| `InMemoryUnitOfWork` | In-memory `UnitOfWork` for transactional consistency and event publication |
| `InMemoryMessageBus` | In-memory `MessageBus` for intra-process message routing |
| `RepositoryError` | Base error for repository operation failures |
| `RepositoryNotFoundError` | Error for missing aggregates on delete/retrieve |

---

## ✨ Guidelines

- **Purpose:** Provide reusable adapters that implement application-layer ports.
- **Design:** Each class in its own file. All implementations are dependency-injectable.
- **SOLID:** Read and write repositories are separated (CQRS), enabling clean read/write split.

---

## 🏗️ Why This Matters

- **Clarity & Cleanliness:** Keeps your toolbox focused and reusable.
- **Separation:** Framework- and project-specific code lives with your app, keeping
  the toolbox easy to maintain.

---

For real-world adapters and usage with frameworks or libraries, see the `/examples` directory.
