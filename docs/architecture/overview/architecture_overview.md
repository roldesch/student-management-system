🏛️ Architecture Overview

The Student Management System (SMS) follows Clean Architecture combined with Domain-Driven Design (DDD).

The system is organized into four layers with strict dependency rules that preserve domain isolation and long-term evolvability.

+--------------------------------------------------+
|                  Presentation                    |
|--------------------------------------------------|
| CLI Interface                                    |
| - Command parsing                                |
| - Error rendering                                |
| - Output formatting                              |
+--------------------------------------------------+
                        │
                        ▼
+--------------------------------------------------+
|                Application Layer                 |
|--------------------------------------------------|
| Use-case orchestration                           |
|                                                  |
| Core component                                   |
| - StudentManagementSystem (application service)  |
|                                                  |
| Boundary mechanisms                              |
| - DTOs (input contracts)                         |
| - Application validation                         |
| - Response Models (immutable outputs)            |
| - Mapping logic (domain → response translation)  |
+--------------------------------------------------+
                        │
                        ▼
+--------------------------------------------------+
|                   Domain Layer                   |
|--------------------------------------------------|
| Core business model and rules                    |
|                                                  |
| - Entities: Student, Teacher, Course             |
| - Aggregate root: Course                         |
| - Domain exceptions                              |
| - Repository interfaces                          |
+--------------------------------------------------+
                        ▲
                        │
+--------------------------------------------------+
|               Infrastructure Layer               |
|--------------------------------------------------|
| Persistence and external integrations            |
|                                                  |
| - In-memory repositories                         |
| - SQLite repositories                            |
| - Transaction coordination                       |
| - Row mappers and schema bootstrap               |
+--------------------------------------------------+
Dependency Direction

Dependencies always point toward the domain layer.

Presentation → Application → Domain
Infrastructure → Domain

The Domain layer depends on nothing outside itself, ensuring that business logic remains pure and independent of frameworks or infrastructure.

This isolation is a core architectural constraint of the system.

Application Boundary

The Application Layer acts as the boundary between external consumers and the internal domain model.

Application services orchestrate use cases but do not implement business rules.

Inbound Flow

External input enters the system as DTOs.

CLI
  ↓
DTO
  ↓
Application Service

Application services perform application-level validation before invoking domain logic.

Validation checks:

input structure

primitive value validity

basic semantic constraints

Application validation never enforces business rules.

Domain Execution

Once validation succeeds, the application service orchestrates domain behavior.

Application Service
  ↓
Domain Entities / Aggregates
  ↓
Repository Interfaces

Business rules and invariants are enforced exclusively inside domain entities.

The Course entity acts as the aggregate root governing:

student enrollment

teacher assignment

relationship consistency

This design explicitly rejects an anemic domain model.

Outbound Flow

Domain entities never leave the application layer.

Instead, results are converted to immutable Response Models.

Domain Entities
  ↓
Response Mapping
  ↓
Response Models
  ↓
CLI

Response Models represent use-case outcomes and contain only primitives and immutable collections.

This protects the domain model from accidental mutation by external layers.

Error and Exception Semantics

Failures are classified according to the layer where they originate.

Application Errors

Raised when input is invalid.

Examples:

ApplicationValidationError

These occur before domain execution.

Domain Errors

Raised when business rules are violated.

Examples:

EnrollmentError

TeacherAssignmentError

Domain errors originate only from domain entities and propagate unchanged.

Repository / State Errors

Raised when persistence conditions fail.

Examples:

EntityNotFoundError

DuplicateIdentityError

Repositories represent persistence concerns only and never enforce business rules.

Persistence Strategy

Repository interfaces are defined in the Domain Layer.

Concrete implementations live in Infrastructure.

infrastructure/
 ├─ in_memory/
 └─ sqlite/

SQLite infrastructure includes:

schema bootstrap

row mappers

transaction coordination

repository implementations

Repositories reconstruct domain entities using constructor-safe reconstruction, ensuring persistence remains decoupled from domain logic.

Testing Architecture

The test suite mirrors the system architecture:

tests/
 ├─ domain
 ├─ application
 ├─ infrastructure
 ├─ integration
 ├─ system
 └─ contracts

Each test layer verifies the behavior of its corresponding architectural layer while preserving strict isolation boundaries.

Tests enforce architectural rules but do not define them.

Architectural truth is defined by ADRs and implementation.

Current Architectural Phase

The system currently operates in the DTO + Application Boundary phase, characterized by:

immutable DTO inputs

immutable Response Models

strict application boundary enforcement

explicit application-level validation

backend-agnostic repository contracts

This architecture prepares the system for future extensions such as:

REST APIs

additional persistence backends

distributed service integration

without compromising domain integrity.