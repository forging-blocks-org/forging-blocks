# Reference
## Overview of ForgingBlocks Components

```mermaid
flowchart LR
    D[Domain<br/>Problem-space concepts] -->|depends on| F[Foundation<br/>Shared abstractions]
    A[Application<br/>Coordination & behavior] -->|depends on| D
    A -->|depends on| F
    I[Infrastructure<br/>Technical adapters] -->|depends on| A
    I -->|depends on| F
    P[Presentation<br/>Input boundaries] -->|depends on| A
```

## Reference Sections

- **[Foundation](foundation.md)** - Core abstractions and utilities (Result, Port, etc.)
- **[Domain](domain.md)** - Domain modeling abstractions (Entity, ValueObject, AggregateRoot)
- **[Application](application.md)** - Application layer patterns (UseCase, CommandHandler)
- **[Infrastructure](infrastructure.md)** - Infrastructure adapters and implementations
- **[Presentation](presentation.md)** - Input/output boundaries and presentation layer
- **[Testing](testing.md)** - Comprehensive testing reference and guidelines
