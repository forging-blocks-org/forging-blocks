# Hexagonal Architecture (Ports & Adapters)

!!! note "Important"
    ForgingBlocks does **not** require Hexagonal Architecture.
    Hexagonal Architecture focuses on isolating the core domain behind ports, with adapters surrounding it.

---

# 1. Core Hexagonal Model

```mermaid
flowchart LR
    AdapterIn[Inbound Adapter<br/>REST • CLI • Message Listener] --> InPort[Inbound Port]
    InPort --> ApplicationService[Application Service]
    ApplicationService --> DomainCore[Domain Core<br/>Aggregates • Entities • Value Objects • Events]
    ApplicationService --> OutPort[Outbound Port]
    OutPort --> AdapterOut[Outbound Adapter<br/>Database • API • Email • MQ]
```

---

# 2. Hexagon Shape Representation

```mermaid
flowchart TB
    InAdapters[Inbound Adapters] --> Core[Domain + Application Core]
    OutAdapters[Outbound Adapters] --> Core
```

---

# 3. Key Points

- Domain Core is the **center** of the hexagon.
- Communication happens only through **ports**, never directly.
- Adapters are replaceable.
- The architecture is driven by **runtime boundaries**, not concentric layers.
