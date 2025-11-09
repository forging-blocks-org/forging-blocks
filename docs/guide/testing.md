# Testing 🧪

> For a hands-on look at real test examples for each layer, see [Example
> Tests](example_tests.md).

The **BuildingBlocks** toolkit encourages a testing strategy that
mirrors its architecture.\
Each layer --- from Foundation to Infrastructure --- can be tested
independently using predictable patterns and explicit contracts.

------------------------------------------------------------------------

## 🧱 Domain Layer

-   Test **pure business logic** with no external dependencies.
-   Use **value objects**, **entities**, and **aggregates** in
    isolation.
-   Validate **invariants**, **rules**, and **domain events**.

> Domain tests should not depend on frameworks or infrastructure.

------------------------------------------------------------------------

## ⚙️ Application Layer

-   Test **use cases** through their **inbound ports** (interfaces).
-   Mock outbound dependencies such as repositories or event buses.
-   Validate that each use case produces the expected **Result** type
    (Ok/Err).

> Application tests focus on orchestration --- not persistence.

------------------------------------------------------------------------

## 🧩 Infrastructure Layer

-   Test **adapters** (repositories, event publishers, message buses).
-   Use **in-memory** or **temporary database** fixtures when
    appropriate.
-   Verify correctness of integration with external systems.

> Keep infrastructure tests focused on technical boundaries.

------------------------------------------------------------------------

## 🧠 General Guidelines

-   Follow the **AAA pattern** (Arrange → Act → Assert).
-   Use **pytest** fixtures for clean, reusable setup.
-   Prefer **behavioral** assertions (what the code does) over
    structural ones (how it does it).
-   Each test name should clearly express intent using:\
    `test_<method>_WHEN_<scenario>_THEN_<expected_result>`

------------------------------------------------------------------------

Testing in **BuildingBlocks** is about clarity and intent --- ensuring
that each layer is verified independently, without leaking concerns
across architectural boundaries.
