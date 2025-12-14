# Clean Architecture

!!! note "Important"
    ForgingBlocks does **not** require Clean Architecture.

    Clean Architecture is a structured variant of layered/hexagonal principles emphasizing strict inward dependencies and explicit use cases.

---

# 1. Clean Architecture — Layer Responsibilities


```mermaid
flowchart LR
    PresentationLayer["Presentation Layer<br/>Controllers • Handlers • UI"] --> ApplicationLayer["Application Layer<br/>Use Cases • Interactors"]
    ApplicationLayer --> DomainLayer["Domain Layer<br/>Aggregates • Entities • Value Objects • Events"]
    ApplicationLayer --> OutboundPorts["Outbound Ports <br/>(Output Boundaries)"]
    InboundPorts["Inbound Ports<br/>(Input Boundaries)"] --> ApplicationLayer
    OutboundPorts --> InfrastructureLayer["Infrastructure Layer<br/>Adapters • Implementations"]
```

---

# 2. Domain Composition

```mermaid
flowchart TB
    Aggregate[Aggregate] --> Entity[Entities]
    Entity --> ValueObject[Value Objects]
    Aggregate --> Event[Events]
```

---

# 3. Ports & Adapters (Clean Architecture)

```mermaid
flowchart LR
    Presentation["Presentation Layer"]
        --> InputBoundary["Inbound Port<br/>(Input Boundary)"]

    InputBoundary
        --> UseCase["Application Service<br/>Use Case Interactor"]

    UseCase
        --> OutputBoundary["Outbound Port<br/>(Output Boundary)"]

    OutputBoundary
        --> Adapter["Infrastructure Adapter"]
```



---

# 4. Summary

Clean Architecture is a refined layered model with strict dependency direction and explicit use cases.

ForgingBlocks integrates cleanly with this structure without enforcing it.

---

# 5. Traditional Clean Architecture Diagram

![Clean Architecture – Concentric Model](../assets/svg/clean-architecture.svg)
