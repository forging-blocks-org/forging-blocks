# Reference 📖

> **Audience:** Contributors and maintainers of **BuildingBlocks** who
> want to understand its internal design, structure, and abstractions.

The **Reference** section documents the internal components of
**BuildingBlocks** --- what each package contains, how they depend on
one another, and how they fit into the overall architecture.

It is primarily useful for developers extending or improving the toolkit
itself.

------------------------------------------------------------------------

## 🧩 Package Overview

  -----------------------------------------------------------------------
  Package                       Description
  ----------------------------- -----------------------------------------
  **Foundation**                Core abstractions (`Result`, `Port`,
                                `Mapper`) shared across all layers

  **Domain**                    Encapsulates business rules and the
                                ubiquitous language

  **Application**               Defines use cases and application logic
                                through inbound and outbound ports

  **Infrastructure**            Implements adapters for external systems
                                (e.g., databases, events, APIs)

  **Presentation**              Provides entry points (HTTP API, CLI, or
                                message consumers)
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 📚 Contents

-   [Foundation](foundation.md)
-   [Domain](domain.md)
-   [Application](application.md)
-   [Infrastructure](infrastructure.md)
-   [Presentation](presentation.md)
-   [Example Tests](../guide/example_tests.md)
