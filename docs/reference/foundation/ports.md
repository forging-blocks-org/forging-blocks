# Ports

Ports define **boundaries** between components — what is expected, not how it is implemented.
They enforce architectural dependency direction at **class-definition time** through
``__init_subclass__`` validation.

## Port

`Port` is the root abstract base class for the hierarchy. It uses `FinalABCMeta`
(which combines `ABCMeta` with runtime-final enforcement) and declares
``__init_subclass__`` as an abstract method. This forces every subclass —
`InboundPort`, `OutboundPort`, and all concrete ports — to participate in the
``__init_subclass__`` chain, creating the hook where dependency-direction rules
are enforced.

```python
from forging_blocks.foundation.ports import Port

class Port(ABC, metaclass=FinalABCMeta):
    @classmethod
    @abstractmethod
    def __init_subclass__(cls, /) -> None: ...
```

Application code should **never** subclass `Port` directly — extend `InboundPort`
or `OutboundPort` instead.

## InboundPort

`InboundPort` extends `Port` and marks the **driving side** of the hexagon:
use cases, message handlers, presenters — anything infrastructure calls *into*.

Its ``__init_subclass__`` is decorated ``@runtime_final`` and runs
``InboundDependencyValidator`` on every concrete subclass. The validator compares
declared ``PortLevel`` values: an inward dependency is allowed, while an outward,
same-level, or unknown-level dependency raises ``ArchitectureError``. Without
declared levels, an inbound port may not depend on another inbound port.

## OutboundPort

`OutboundPort` extends `Port` and marks the **driven side** of the hexagon:
repositories, event buses, loggers, caches — anything the application core
calls *out to*.

Its ``__init_subclass__`` is decorated ``@runtime_final`` and runs
``OutboundDependencyValidator`` on every concrete subclass. The validator applies
the same level-aware rule: inward dependencies are allowed, while outward,
same-level, or unknown-level references to inbound ports raise ``ArchitectureError``.
Outbound ports may otherwise depend on outbound ports.

## check_methods

``check_methods(subclass, *method_names)`` is a utility for
``__subclasshook__`` consumers. It returns ``True`` when *subclass* has
all the named callable attributes, enabling structural subtype checks
without explicit inheritance.

## When to use

Extend `InboundPort` for contracts that define how a component is called.
Extend `OutboundPort` for contracts that define what a component depends on.
The ``__init_subclass__`` validation catches architectural drift at the point
of definition — no runtime check, no CI plugin needed.

!!! note "Related"
    See [Application Ports](../application/ports.md) for concrete inbound and outbound port definitions.
