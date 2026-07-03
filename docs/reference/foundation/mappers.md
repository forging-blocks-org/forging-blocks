# Mappers

A **Mapper** is an explicit transformation between two types. It makes type conversion visible and testable.

## Protocol

`Mapper[SourceType, TargetType]` defines a single method: `map(source) → target`. It is a Protocol — any callable or object that satisfies the shape qualifies.

## When to use

Use `Mapper` when data crosses a boundary: entity → DTO, DTO → domain object, persistence model → read model. It keeps transformation logic in one place rather than scattered across call sites.
