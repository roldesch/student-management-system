# ADR-00R — Repository Contract Formalization and Backend Parity

## Status

Accepted

---

## Context

SQLite persitence integration Phase-4 of the Student Management System (SMS) introduced SQLite-backed persistence as the first real infrastructure implementation of repository interfaces.

Prior to this phase:

- Repository interfaces existed but were **not bound by contract tests**.
- In-memory repositories:
  - Were implemented opportunistically.
  - Raised **domain errors** in cases that should semantically be **repository/state errors**.
- No explicit repository contract had been mechanically enforced across backends.

Phase-4 originally assumed that:

> Existing repository behavior was already contract-compliant and backend-agnostic.

That assumption was false.

The introduction of SQLite persistence revealed a latent architectural fork:

- SQLite repositories correctly raised repository/state errors.
- In-memory repositories violated ADR-00Z by raising domain errors.
- Contract tests failed unless weakened to accept both.

Allowing mixed error semantics would redefine the repository contract incorrectly and introduce architectural drift.

This ADR exists to resolve that fork explicitly and to formalize the correct execution of Phase-4 without weakening architectural rules.

---

## Decision

### 1. Repository Contract Semantics Are Fixed and Strict

The repository contract is defined as follows:

- Repositories raise **repository/state errors only**.
- Domain errors:
  - Are raised **only by domain entities**.
  - Must not be raised, translated, or proxied by repositories.

Examples:

- `get(missing_id)` → repository/state error
- `add(duplicate_id)` → repository/state error

This contract is consistent with:

- ADR-00Y — Repository Role and Limitations
- ADR-00Z — Error and Exception Taxonomy

It is **not negotiable** and must not be weakened to accommodate legacy implementations.

---

### 2. Phase-4 Is Explicitly Split Into Two Sub-Phases

Phase-4 is reinterpreted as two explicit and ordered sub-phases.

#### Phase-4A — SQLite Contract Baseline (Current)

**Goal**  
Establish the correct repository contract using SQLite as the first honest persistence backend.

**Rules**

- Repository contract tests:
  - Assert **repository/state errors only**.
  - Must remain strict and normative.
- Tests are executed primarily against SQLite repositories.
- In-memory repository failures are:
  - Acknowledged.
  - Explicitly documented.
  - Not normalized into the contract.

**Temporary Enforcement Handling (Allowed)**

One of the following may be used **explicitly and temporarily**:

- Mark known in-memory failures as `xfail`.
- Scope contract test execution to SQLite only.

These mechanisms exist solely to unblock Phase-4A and **must not** redefine the repository contract.

---

#### Phase-4B — Cross-Backend Contract Parity (Mandatory Next)

**Goal**  
Retroactively formalize the repository contract across all backends.

**Required Actions**

- Refactor in-memory repositories to:
  - Raise repository/state errors.
  - Comply fully with the established contract.
- Remove all temporary enforcement guards:
  - `xfail`
  - Backend-specific execution scopes

**Outcome**

- The **same contract tests**, unchanged, pass against:
  - SQLite repositories
  - In-memory repositories

Phase-4B is **mandatory** and must be completed before declaring repository behavior backend-agnostic.

---

### 3. Tests Remain Enforcement Mechanisms, Not Contract Authors

Consistent with ADR-00T:

- Tests do not define architecture.
- Tests enforce architectural decisions made elsewhere.
- Temporary suspension of enforcement does not weaken the contract.

Any test that permanently accepts mixed domain/repository error semantics is architecturally invalid.

---

## Consequences

### Positive

- Architectural correctness is preserved.
- SQLite integration proceeds without corrupting error semantics.
- Repository contracts become explicit and backend-agnostic.
- Missed early formalization is corrected transparently.

### Trade-offs

- Temporary inconsistency between repository implementations.
- Additional refactoring work deferred to Phase-4B.

These trade-offs are intentional, documented, and time-bounded.

---

## Enforcement

The following are architectural violations:

- Weakening repository contract tests to accept domain errors.
- Treating mixed error behavior as acceptable or permanent.
- Completing Phase-4 without executing Phase-4B.

Any such occurrence must be treated as an architectural defect, not a pragmatic choice.

---

## Relationship to Other ADRs

This ADR clarifies execution sequencing and **does not override**:

- ADR-00Y — Repository Role and Limitations
- ADR-00Z — Error and Exception Taxonomy
- ADR-00T — Testing Policy and Boundaries

It makes an implicit Phase-4 assumption **explicit and enforceable**.

---

## Summary

SQLite persistence exposed an unresolved architectural fork.

This ADR resolves it by:

- Fixing the repository contract unambiguously.
- Allowing controlled, explicit temporary enforcement suspension.
- Mandating full backend parity as a follow-up phase.

> **Architecture is defined by truth, not by legacy behavior.**

