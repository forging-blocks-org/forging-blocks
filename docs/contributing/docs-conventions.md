# Documentation Conventions

## Who this document is for

This document is for contributors who are **writing or modifying documentation** in the ForgingBlocks repository.

It defines the conventions used across the documentation.
These rules are intentional and should be followed consistently.

---

## General principles

Documentation favors:

- Explicit behavior over implied behavior.
- Clear responsibility boundaries.
- Neutral, non-prescriptive language.
- Consistency across sections and pages.

The goal is to help readers reason, not to persuade them.

---

## Tone and language

- Use a professional, calm, and teachable tone.
- Avoid marketing language.
- Avoid enforcing architectural choices.
- Prefer “can” and “may” over “should” and “must” unless stating a rule.

Documentation should explain *why* something exists before explaining *how*.

---

## Structure and formatting

- Headings should describe responsibility or intent.
- Bullet points must:
  - Start with an uppercase letter.
  - Contain exactly one sentence.
  - End with a period.
- Do not break lines unless a sentence ends.

Consistency matters more than individual style preferences.

---

## Diagrams

- Diagrams are explanatory, not prescriptive.
- Diagrams must not be the last content in a document.
- Inline SVG is not allowed in Markdown.
- SVG diagrams must be stored as assets and referenced as images.

Diagrams should clarify relationships, not introduce new rules.

---

## Sections and responsibilities

- **Guide** pages are teachable and narrative.
- **Reference** pages are precise and definition-oriented.
- **Architectural Styles** pages are interpretive and optional.
- **Examples** demonstrate usage without enforcing structure.

Do not blur these responsibilities.

---

## When changing existing documentation

When modifying documentation:

- Preserve the original intent.
- Avoid introducing new terminology casually.
- Update related sections if behavior or meaning changes.
- Prefer small, focused edits.

If a change requires explanation, add context explicitly.

---

## In short

- These conventions are deliberate.
- Consistency is more important than creativity.
- When in doubt, match existing documentation.

This document acts as a shared contract between contributors.
