# Permissions

Composable permission-checking strategies for authorization decisions. Each checker evaluates an application-defined context against a specific `Permission` and returns `True` when granted.

## PermissionChecker

`PermissionChecker[PermissionCheckContext]` is a `Protocol` that any permission-checking implementation must satisfy. The context type is provided by the application.

```python
class PermissionChecker[PermissionCheckContext](Protocol):
    async def check(self, context: PermissionCheckContext, permission: Permission) -> bool:
        ...
```

Implementations may internally use synchronous logic, but must expose an `async def check(...)` method — callers always `await` the result.

## CompositePermissionChecker

Combines multiple `PermissionChecker[PermissionCheckContext]` instances with OR logic. A check passes as soon as **any** inner checker approves. Returns `True` immediately on the first success; otherwise `False` after all checkers have been consulted.

```python
checker = CompositePermissionChecker([
    my_role_checker,
    my_resource_checker,
])
result = await checker.check(context, Permission.READ)
```

## Designing your own checkers

Applications define concrete `PermissionChecker` implementations that inspect their own context type. A role-based checker might look up permissions from a role-to-permission mapping:

```python
from forging_blocks.domain.permissions import PermissionChecker

class RoleBasedChecker[PermissionCheckContext](PermissionChecker[PermissionCheckContext]):
    def __init__(self, role_map: dict[str, list[Permission]]) -> None:
        self._role_map = role_map

    async def check(self, context: PermissionCheckContext, permission: Permission) -> bool:
        roles = getattr(context, "roles", [])
        for role in roles:
            if permission in self._role_map.get(role, []):
                return True
        return False
```

A resource-based checker would similarly inspect resource metadata on the context object.

## When to use

Use `CompositePermissionChecker` to combine multiple checkers when authorization depends on multiple factors — an admin role OR ownership of a document, for example. Define application-specific `PermissionChecker` subclasses for role-driven authorization (RBAC), resource-level access control, or any custom authorization logic.

All checkers operate on the foundation `Permission` type and an application-defined context, keeping the domain free of infrastructure concerns.

!!! note "Related"
    Permissions use the `Permission` enum (in `forging_blocks.foundation.permission`). See [Foundation Errors](../foundation/errors.md) for error types.
