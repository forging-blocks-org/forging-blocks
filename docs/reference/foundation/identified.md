# Identified

`Identified` is a structural protocol for any object that carries an identifier.

## Protocol

Requires a single property: `id` — returning an identifier that may be `None` for a draft. The protocol does not enforce uniqueness or lifecycle rules; those belong to the implementing type.

## When to use

`Identified` is used by repositories, mappers, and message types that need to reference objects by identity without depending on a specific entity class.
