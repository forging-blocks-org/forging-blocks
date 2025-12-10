# Domain Layer Reference

## Overview
The domain layer expresses the core business rules and invariants of the system, using Entities, Value Objects, Aggregate Roots, and Domain Messages (Commands, Events, Queries). It is entirely decoupled from infrastructure and frameworks.

## Entities
Entities are defined by identity and feature strong invariants: identity is immutable once set, equality is based strictly on id, and draft entities (id=None) are not hashable.

## Value Objects
Value objects are immutable and defined only by their value. After initialization, they freeze and cannot be mutated.

## Aggregate Roots
Aggregate Roots enforce consistency boundaries, track versioning using AggregateVersion, and record domain events. Calling collect_events returns the events and increments the version.

## Domain Messages
Messages are immutable and include metadata. Commands express intent, Events express facts, Queries express retrieval requests.

## Domain Errors
Errors enforce domain invariants such as EntityIdNoneError and DraftEntityIsNotHashableError.
