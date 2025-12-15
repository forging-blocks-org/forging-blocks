```mermaid
---
title: Clean Architecture
---
graph TD
    subgraph outer["Frameworks & Drivers"]
        subgraph adapters["Interface Adapters"]
            subgraph app["Application Business Rules"]
                subgraph core["Enterprise Business Rules"]
                end
            end
        end
    end
```
