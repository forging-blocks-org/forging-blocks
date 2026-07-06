# Permissions

Composable permission-checking strategies for authorization decisions. Each checker evaluates an `AuthorizationContext` against a specific `Permission` and returns `True` when granted.

## PermissionChecker

`PermissionChecker` is a `Protocol` that any permission-checking implementation must satisfy.

```python
class PermissionChecker(Protocol):
    async def check(self, context: AuthorizationContext, permission: Permission) -> bool:
        ...
```

Implementations may internally use synchronous logic, but must expose an `async def check(...)` method — callers always `await` the result.

## RoleBasedPermissionChecker

Grants permissions based on a static mapping of roles to allowed permissions. Looks up the user's roles in the `AuthorizationContext` and checks whether any assigned role includes the requested permission.

```python
checker = RoleBasedPermissionChecker({
    "admin": [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
    "editor": [Permission.READ, Permission.WRITE],
})
```

## ResourcePermissionChecker

Grants permissions based on a static mapping of resource types to allowed permissions. Inspects `AuthorizationContext.resource_type` and checks whether the targeted resource type permits the requested permission.

```python
checker = ResourcePermissionChecker({
    "document": [Permission.READ, Permission.WRITE],
    "image": [Permission.READ],
})
```

## CompositePermissionChecker

Combines multiple `PermissionChecker` instances with OR logic. A check passes as soon as **any** inner checker approves. Returns `True` immediately on the first success; otherwise `False` after all checkers have been consulted.

```python
checker = CompositePermissionChecker([
    RoleBasedPermissionChecker({"admin": [Permission.READ]}),
    ResourcePermissionChecker({"document": [Permission.READ]}),
])
```

## When to use

Use `RoleBasedPermissionChecker` for role-driven authorization (RBAC). Use `ResourcePermissionChecker` for resource-level access control. Combine them with `CompositePermissionChecker` when authorization depends on multiple factors — an admin role OR ownership of a document, for example.

All checkers operate on the foundation `AuthorizationContext` and `Permission` types, keeping the domain free of infrastructure concerns.

!!! note "Related"
    See [Foundation Context](../foundation/context.md) for `AuthorizationContext` and `Permission`, and [Foundation Errors](../foundation/errors.md) for error types.
