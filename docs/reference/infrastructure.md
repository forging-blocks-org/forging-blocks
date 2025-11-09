# Infrastructure Package 🏗️

The **infrastructure** package contains *technical implementations* of outbound ports defined in the application layer.

---

## 🧠 Purpose

Implements **adapters** that connect the application to external systems such as databases, APIs, and message brokers.

---

## ⚙️ Components

### Repository Implementations

```python
class SqlUserRepository(UserRepository):
    '''SQL-based implementation of the UserRepository outbound port.'''
    async def save(self, user: User) -> None:
        '''Persist a user to the database.'''
        await db.execute("INSERT INTO users (id, username, email) VALUES (:id, :username, :email)", user.to_dict())
```
---
