# Presentation Package 🧩

The **presentation** package is the system’s *entry point*.  
It handles user or system interactions and delegates execution to the **application layer**.

---

## 🧠 Purpose

Implements **inbound adapters** such as APIs, CLI commands, or event consumers.

---

## ⚙️ Components

### REST API Controllers

```python
@router.post("/users")
async def register_user(request: RegisterUserRequest) -> Response:
    '''HTTP endpoint for user registration.'''
    result = await register_user_service.execute(request.to_dto())
    if result.is_ok():
        return Response(result.value, status_code=201)
    return Response({"error": result.error.reason}, status_code=400)
```
---
