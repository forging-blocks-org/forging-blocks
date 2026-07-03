# Ports

Ports define **boundaries** between components — what is expected, not how it is implemented.

## Port

`Port` is the base protocol. All ports extend it. It carries no methods — a marker for architectural intent.

## InboundPort

`InboundPort` extends `Port`. Marks how a component is called: use cases, message handlers, presenters.

## OutboundPort

`OutboundPort` extends `Port`. Marks what a component needs: repositories, event buses, loggers, caches. Infrastructure implements these.

## When to use

Extend `InboundPort` for protocols that define how a component is called. Extend `OutboundPort` for protocols that define what a component depends on. These are markers — they carry no methods. They communicate architectural role to readers and tooling.

!!! note "Related"
    See [Application Ports](../application/ports.md) for concrete inbound and outbound port definitions.
