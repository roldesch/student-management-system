# ADR-005: Freeze CLI Surface (Phase 0)

## Status

**Accepted**

## Phase

**Phase 0 — Versioning Discipline**

---

## Context

The Student Management System (SMS) has reached a stable state with:

* A complete and fully passing test suite
* A production-ready CLI
* A strict application boundary (DTOs, response models)
* Explicit application-level validation
* Deterministic exit codes and error classification

The CLI now represents the **primary public interface** of the system.
Without an explicit versioning and compatibility policy, future evolution risks accidental breaking changes to user-facing behavior.

---

## Decision

The **CLI surface is formally frozen as of SMS v1.0.0**.

This decision establishes the CLI as a **stable, versioned public contract** governed by semantic versioning rules.

A minimal `--version` command is introduced to expose the current CLI version and anchor compatibility guarantees.

---

## Definition of the CLI Surface (Normative)

The CLI surface includes:

* Command names and structure
  (e.g. `sms student add`, `sms enroll`, `sms --version`)
* Required and optional arguments
* Exit codes and their meanings
* Error classification (validation vs domain vs state errors)
* Output intent (human-readable, deterministic)

The CLI surface explicitly **excludes**:

* Internal implementation details
* Domain model structure
* Repository or infrastructure choices
* Output formatting aesthetics (unless documented)

---

## Versioning Rules

SMS follows **Semantic Versioning** at the CLI level.

### Breaking Changes (Require MAJOR version bump)

* Removing or renaming commands
* Changing command argument semantics
* Changing exit codes or their meaning
* Changing error classification boundaries
* Allowing domain entities to escape the application boundary
* Altering the meaning of existing output fields

### Non-Breaking Changes (MINOR or PATCH)

* Adding new commands
* Adding optional flags
* Adding new infrastructure backends
* Performance improvements
* Internal refactoring with identical observable behavior

---

## Guarantees Introduced

As of this ADR:

* `sms --version` MUST exist and succeed
* Exit codes are deterministic and stable
* CLI behavior is backward compatible within a major version
* All future changes MUST declare their compatibility impact

---

## Consequences

### Positive

* Establishes a clear public contract
* Enables safe evolution (JSON export, persistence, API)
* Prevents accidental breaking changes
* Increases confidence for users and scripts

### Trade-offs

* Requires discipline when evolving the CLI
* Some refactors may require a major version bump

These trade-offs are accepted as necessary for system maturity.

---

## Relationship to Other Decisions

* Complements DTO boundary refactoring (ADR-001, ADR-002, ADR-003)
* Precedes future decisions on persistence, JSON import/export, or APIs
* Forms the foundation for any future external integrations

---

## Enforcement

* CLI contract tests MUST exist for frozen behaviors
* Any breaking change MUST increment the major version
* This ADR MUST be revisited only if the CLI is deprecated or replaced

---

## Summary

This ADR marks the transition of SMS from a development project to a **governed system**.

From this point forward, the CLI is a **stable interface**, not an implementation detail.
