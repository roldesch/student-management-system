# Application DTO Refactoring Initiative

## Overview

This document group describes the introduction of **Application-Layer Data Transfer Objects (DTOs)** and related patterns in the Student Management System (SMS).

The goal is to establish a **clean, stable, and explicit boundary** between:

- The **Domain Layer** (rich entities, invariants, aggregates)
- The **Application Layer** (use case orchestration)
- The **Presentation Layer** (CLI / UI / API)

We do this by introducing **immutable DTOs** and, in later phases, **mutable use-case response models** and **DTO mappers**.

## Motivation

Currently, the Application Service (`StudentManagementSystem`) exposes **domain entities directly**. This causes:

- Tight coupling between domain internals and UI/CLI/tests.
- Increased risk of accidentally mutating aggregates from outside.
- Fragile public contracts: any domain shape change breaks callers.
- Violation of Clean Architecture: entities should be internal to the core.

DTOs provide:

- A **flat, serialization-friendly** representation of domain state.
- **Immutable snapshots** suitable for CLI/API/UI.
- A **long-lived contract** decoupled from internal domain changes.

## Phased Plan

This initiative is intentionally split into phases:

1. **Phase 1 – DTO Design and Introduction**
   - Introduce immutable DTOs in `application/dtos/`
   - No changes yet to `StudentManagementSystem` behavior.
   - No response models or mappers implemented yet.
   - Fully backward-compatible.

2. **Phase 2 – DTO Mappers and Use-Case Response Models**
   - Implement mappers from Domain → DTO in `application/mappers/`.
   - Introduce mutable response models in `application/responses/`.
   - Prepare the application service to return DTOs/Response Models.

3. **Phase 3 – Application Service Refactor**
   - Refactor `StudentManagementSystem` to:
     - Return DTOs for query-like operations.
     - Return Response Models for command-like operations (enroll, assign teacher, grade, etc.).

4. **Phase 4 – CLI / UI Integration**
   - Implement a CLI (and possibly later a REST API) which:
     - Calls application services.
     - Consumes DTOs and response models.
     - Never touches domain entities directly.

5. **Phase 5 – Optional Migration to Pydantic**
   - If/when a REST API is added, DTOs may be migrated from `dataclasses` to Pydantic `BaseModel` without affecting domain or application logic.

## Folder Structure

New relevant folders:

```text
application/
    dtos/
        __init__.py
        student_dto.py
        teacher_dto.py
        course_dto.py

    responses/   # (created in Phase 2)
        __init__.py
        ...
