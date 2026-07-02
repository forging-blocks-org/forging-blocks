# Domain Errors

Domain Errors represent invalid states or rule violations within the problem space. They express domain meaning, indicate invariant violations, and are not technical failures.

They extend the Foundation `Error` base class and carry structured messages and metadata.

!!! note "On error semantics"
    Domain Errors describe *why* something is invalid in domain terms. They should not encode transport, persistence, or framework concerns.
