# Ports

Ports define **boundaries** between components — what is expected, not how it is implemented.

## Port

`Port` is the base protocol. All ports (inbound and outbound) extend it. It carries no methods — it is a marker for architectural intent.

## InboundPort

`InboundPort` extends `Port`. It marks protocols that define how a component is called — use cases, message handlers, presenters.

## OutboundPort

`OutboundPort` extends `Port`. It marks protocols that define what a component needs — repositories, event buses, loggers, caches. Infrastructure implements these.

!!! note "Related"
    See [Application Ports](../application/ports.md) for concrete inbound and outbound port definitions.
