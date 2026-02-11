ADR-004 — Intentional Constructor Coupling for Transactional Isolation

Status: Accepted
Date: 2026-02-11
Phase: Phase-5 — Composition Root Wiring

Context

Phase-5 introduces SqliteTransactionalStudentManagementSystem, an infrastructure-owned transactional proxy responsible for:

Opening exactly one UnitOfWork per use-case call

Constructing transaction-bound SQLite repositories

Instantiating a fresh StudentManagementSystem

Delegating the call and returning the result verbatim

To guarantee strict transactional isolation, the proxy constructs StudentManagementSystem inside infrastructure on every invocation.

This creates constructor coupling:

Infrastructure depends on the concrete constructor signature of the application service.

This coupling is deliberate and must be evaluated explicitly.

Problem

Instantiating the application service inside infrastructure introduces:

Direct dependency on the constructor signature

Required synchronization when the constructor changes

Infrastructure awareness of application construction details

Without documentation, this may be misinterpreted as accidental or refactored away improperly.

Decision

The architecture intentionally accepts constructor coupling between:

SqliteTransactionalStudentManagementSystem (infrastructure)

StudentManagementSystem (application)

This decision prioritizes:

Strict per-use-case transactional isolation

Prevention of cross-call state leakage

Elimination of repository rebinding complexity

Over:

Constructor decoupling

Long-lived service reuse

Isolation is considered more critical than construction flexibility.

Rationale

Each use case must:

Run inside its own UnitOfWork

Use repositories bound to that transaction’s connection

Avoid any mutable state shared across calls

A long-lived StudentManagementSystem would require:

Repository rebinding

Mutable dependency injection

Complex transaction scoping logic

Increased risk of cross-transaction leakage

Those alternatives introduce higher correctness risk than constructor coupling.

Therefore, the system constructs a fresh service instance per invocation.

Trade-Off Analysis
Dimension	Per-Call Construction (Chosen)	Long-Lived Service (Rejected)
Transaction Isolation	Strong — structural guarantee	Complex — requires rebinding
Cross-Call State Leakage	Impossible	Possible
Constructor Coupling	High	Lower
Change Impact	Proxy must mirror constructor changes	Composition root changes only
Runtime Overhead	Slightly higher	Slightly lower
Correctness Risk	Low	Higher
Boundary Violations	None	None
Cognitive Complexity	Moderate	Higher
Maintenance Invariant

Any change to the constructor signature of StudentManagementSystem:

Must be mirrored in SqliteTransactionalStudentManagementSystem.

Must preserve per-call instantiation.

Must not introduce state caching or reuse.

Failure to maintain this invariant constitutes an architectural defect.

Alternatives Considered
1. Injecting a Service Factory

Instead of constructing the service directly, the proxy could accept:

Callable[..., StudentManagementSystem]


This would reduce direct constructor coupling.

Rejected because:

Introduces unnecessary abstraction for Phase-5

Obscures construction clarity

Increases wiring complexity

Does not reduce transactional coupling

Adds indirection without correctness gain

2. Reusing a Long-Lived Service Instance

Rejected because:

Breaks strict per-call transactional isolation

Requires repository rebinding

Increases risk of subtle state leakage

Makes transaction boundaries implicit rather than structural

Architectural Boundaries

This ADR does not alter:

ADR-00Y — Repository Role and Limitations

ADR-00Z — Error and Exception Taxonomy

ADR-00T — Testing Policy and Boundaries

It clarifies a construction-level trade-off introduced during Phase-5.

Consequences
Positive

Strong transactional correctness guarantees

Structural enforcement of isolation

Reduced mutation complexity

Clear transaction lifecycle ownership

Negative

Constructor coupling between infrastructure and application

Proxy must evolve with service constructor changes

Slight runtime instantiation overhead

These consequences are intentional and bounded.

Enforcement

The following are architectural violations:

Caching or reusing StudentManagementSystem across calls

Rebinding repositories on a long-lived service

Introducing transaction management into the application layer

Abstracting constructor coupling without architectural justification

Per-call service construction is mandatory.

Summary

Phase-5 prioritizes transactional isolation over constructor decoupling.

Constructor coupling is:

Explicit

Intentional

Bounded

Documented

Isolation is enforced structurally, not conventionally.

Correctness and isolation take precedence over construction flexibility.