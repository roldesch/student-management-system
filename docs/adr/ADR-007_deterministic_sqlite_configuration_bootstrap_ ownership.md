# ADR-007 — Deterministic SQLite Configuration and Bootstrap Ownership

## Status

Accepted

---

## Context

During Phase-6 stabilization, it was observed that SQLite database files could be created outside controlled test directories (e.g., project root or system root), depending on execution context.

Although all tests passed, this revealed a silent stability defect:

* SQLite path fallback behavior allowed implicit relative filenames.
* Relative paths were resolved against the current working directory (CWD).
* CWD varies across IDE runs, subprocess tests, CI runners, and developer environments.

This introduced:

* Environment-sensitive filesystem side effects
* Hidden persistence location coupling
* Nondeterministic artifact creation

This ADR formalizes deterministic SQLite configuration rules and clarifies infrastructure bootstrap ownership.

---

## Problem Statement

The CLI entrypoint previously allowed:

```
SMS_BACKEND=sqlite
```

without requiring `SMS_SQLITE_PATH`, defaulting to a relative filename such as:

```
test_sms.db
```

This relative path was resolved using `Path(...).resolve()`, which depends on CWD.

Even though resolution produced an absolute path, the location was still influenced by CWD.

This behavior is incompatible with deterministic infrastructure principles.

---

## Decision

The system adopts the following canonical rules.

---

### 1. No Implicit SQLite Path Fallback

When `SMS_BACKEND=sqlite`, the environment variable `SMS_SQLITE_PATH` **must be explicitly provided**.

If missing, the CLI composition layer must raise a `ConfigurationError`.

There is no relative or filename fallback.

---

### 2. Relative Paths Are Rejected

If `SMS_SQLITE_PATH` is provided but is not absolute, the system must reject it.

Specifically:

* The raw path is parsed.
* If `Path(raw).expanduser().is_absolute()` is `False`, a `ConfigurationError` is raised.
* Only after validation is `resolve()` applied for canonicalization.

This guarantees:

* No CWD-sensitive resolution.
* Full environment independence.
* Deterministic storage location.

---

### 3. Dedicated Configuration Error Type

Missing or invalid SQLite configuration is not:

* A domain error
* A repository/state error
* An application validation error

It is a configuration boundary error.

The CLI/composition layer must define and raise:

```
class ConfigurationError(Exception):
    """Raised when system configuration is invalid before runtime."""
```

This preserves taxonomy clarity and adheres to ADR-00Z.

---

### 4. Canonical Path Normalization Occurs Exactly Once

SQLite path canonicalization occurs at the composition root.

The composition root must:

1. Validate that the path is absolute.
2. Call `.expanduser()`.
3. Call `.resolve()`.
4. Pass the canonical path downward.

Raw or relative paths must never be passed into infrastructure layers.

---

### 5. Bootstrap Ownership — Composition Root Only

`initialize_sqlite_database()` is owned exclusively by the composition root.

Rules:

* The transactional wrapper must not call bootstrap.
* Repository constructors must not call bootstrap.
* UnitOfWork must not call bootstrap.
* Tests must call bootstrap explicitly when bypassing composition root.

Bootstrap must execute exactly once per SQLite backend instantiation.

This ensures:

* Explicit infrastructure readiness
* No duplicate side effects
* Clear ownership
* Reduced coupling

---

### 6. Bootstrap Guardrails

Inside `initialize_sqlite_database()`:

* Canonicalize the provided path.
* If the path exists and is a directory, raise an error.
* Create parent directories if required.
* Apply schema idempotently.

This prevents directory-as-database misuse and future drift.

---

## Enforcement Rules

Violations include:

* Reintroducing a relative filename fallback
* Accepting relative `SMS_SQLITE_PATH` values
* Performing bootstrap in repository constructors
* Performing bootstrap inside transactional wrappers
* Translating configuration errors into application/domain errors

Such violations must be treated as architectural defects.

---

## Testing Requirements

1. CLI tests invoking `main()` with SQLite must set:

   * `SMS_SQLITE_PATH` to an absolute `tmp_path` file.

2. Subprocess CLI tests must provide explicit SQLite path.

3. Add a regression test ensuring:

   * Instantiating repositories alone does not create a database file.

---

## Deferred Considerations

The following are intentionally deferred:

* Providing a deterministic home-directory default (e.g., `~/.sms/sms.db`).
* Multi-process bootstrap race hardening.

These are valid future refinements but are not required for current determinism guarantees.

---

## Consequences

### Positive

* Fully deterministic SQLite persistence location
* No CWD-sensitive behavior
* No silent filesystem side effects
* Clear bootstrap ownership
* Clean error taxonomy

### Trade-offs

* SQLite backend requires explicit configuration
* Relative paths are forbidden
* Slightly stricter CLI configuration requirements

These trade-offs are intentional and accepted.

---

## Summary

This ADR formalizes deterministic SQLite configuration and bootstrap ownership.

It eliminates silent fallback behavior, enforces absolute-path discipline, clarifies error taxonomy boundaries, and centralizes infrastructure readiness.

Determinism is prioritized over convenience.

Status: Accepted and Binding.


