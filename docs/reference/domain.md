# Domain
## Reference

The **Domain** block represents the **problem space** your system is concerned with.

It contains the concepts, rules, and constraints that give meaning to your software,
independent of frameworks, databases, delivery mechanisms, or deployment concerns.

The goal of the Domain block is **clarity of intent**, not architectural purity.

---

## Purpose of the Domain block

The Domain block exists to:

- Express problem-space concepts explicitly
- Encode rules and constraints close to the data they govern
- Make invalid states explicit
- Remain stable as external concerns change

The Domain block depends only on **Foundation** and must not depend on Application, Infrastructure, or Presentation.

---

!!! note "On architectural neutrality"
    ForgingBlocks does not require you to follow a specific architectural style.
    The Domain block can be used in layered, hexagonal, clean, or ad-hoc architectures.
    The abstractions provided here are optional tools, not mandatory patterns.

---

## Core domain abstractions

The Domain block provides **core abstractions** that help model meaning without relying on language primitives alone.

These abstractions exist to make intent explicit, behavior testable, and rules discoverable.

---

## Entities

An **Entity** represents a concept whose **identity** matters over time.

Characteristics:

- Identity-based equality
- Explicit lifecycle
- Mutable state governed by rules

Entities are appropriate when it is important to distinguish *which* instance is being referred to, even if its attributes change.

---

!!! note "Influence: Eric Evans"
    The focus on identity as a defining characteristic is inspired by *Domain-Driven Design* by Eric Evans.
    ForgingBlocks adopts this idea without requiring a full DDD tactical model.

---

## Value Objects

A **Value Object** represents an immutable concept defined entirely by its values.

Characteristics:

- Immutable
- Equality by value
- Hashable
- No independent identity

Value Objects are well-suited for modeling concepts such as identifiers, measurements, or descriptive values where identity is not meaningful.

---

!!! note "Avoiding Primitive Obsession"
    Value Objects help prevent domain rules from being scattered across the codebase.
    By wrapping meaning in explicit types, constraints become visible, reusable, and testable.

---

## Aggregate Roots

An **Aggregate Root** defines a **consistency boundary**.

It acts as the authoritative entry point for modifying related state and enforcing rules that span multiple objects.

Typical responsibilities include:

- Protecting invariants
- Coordinating state changes
- Recording domain-relevant occurrences

---

!!! note "Influence: Vaughn Vernon"
    The emphasis on consistency boundaries and controlled mutation is inspired by the work of Vaughn Vernon.
    ForgingBlocks provides aggregates when boundaries matter, without requiring their use everywhere.

---


## Domain Errors

The Domain block defines **Domain Errors** to represent invalid states or rule violations within the problem space.

Domain Errors:

- Express domain meaning
- Indicate invariant violations
- Are not technical failures

They make incorrect states explicit and testable.

---

!!! note "On error semantics"
    Domain Errors describe *why* something is invalid in domain terms.
    They should not encode transport, persistence, or framework concerns.

---

## What the Domain block does not do

The Domain block does **not**:

- Orchestrate workflows or use cases
- Perform I/O or persistence
- Depend on frameworks or external systems
- Handle transport or presentation concerns

Those responsibilities belong to outer blocks.

---

!!! note "Influence: Robert C. Martin"
    The separation between domain policy and external details reflects principles described by Robert C. Martin.
    The Domain block is intended to be the most stable part of the system.

---

## Summary

The Domain block provides **clear, explicit abstractions** for modeling meaning in the problem space.

You may use all of these abstractions, some of them, or none at all.
Their purpose is to support clarity and correctness—not to enforce a methodology.

---

## Glossary

!!! note "Entity"
    A domain concept with a stable identity that persists over time, even as its attributes change.

!!! note "Value Object"
    An immutable domain concept defined entirely by its values, without independent identity.

!!! note "Aggregate Root"
    A domain concept that defines a consistency boundary and controls access to related state.

!!! note "Domain Error"
    An explicit representation of an invalid domain state or rule violation, expressed in domain terms rather than technical terms.
