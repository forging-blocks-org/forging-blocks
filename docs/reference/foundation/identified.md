# Identified

`Identified` is a structural protocol for any object that carries an identifier.

## Protocol

Requires a single property: `id` — returning a unique identifier for the object. Any class with an `id` property satisfies the protocol automatically.

## When to use

`Identified` is used by repositories, mappers, and message types that need to reference objects by identity without depending on a specific entity class.
