# Student Management System

A Python-based **Student Management System (SMS)** implemented using **Domain-Driven Design (DDD)** and **Clean Architecture** principles.

The project models an academic environment involving **students, teachers, courses, enrollments, and grades**, while enforcing a strict separation of concerns between architectural layers.

This repository is intended as an **educational reference implementation** demonstrating:

* A **rich domain model** with explicit aggregates and invariants
* **Strict application boundaries** enforced through immutable response models
* **Repository-driven persistence abstractions**
* **Layered validation responsibilities**
* A **contract-driven architecture** verified through a comprehensive test suite
* A production-ready **Command-Line Interface (CLI)** acting as a presentation adapter

The system is designed to evolve safely while preserving domain integrity and architectural boundaries.

---

# 🧭 Architecture Overview

The system follows **Clean Architecture** combined with **Domain-Driven Design (DDD)**, organizing responsibilities across four primary layers.

## Domain Layer

The **Domain Layer** contains the core business model and rules of the system.

Responsibilities:

* Core entities (`Student`, `Teacher`, `Course`)
* Business invariants enforced via domain methods
* Domain-specific exceptions for rule violations
* Repository interfaces defining persistence contracts

Key characteristics:

* No dependencies on infrastructure, frameworks, or presentation code
* Rich domain model (not anemic)
* Aggregate ownership enforced through the `Course` entity

Business rules live **exclusively in the domain model**.

---

## Application Layer

The **Application Layer** orchestrates system use cases.

Responsibilities:

* Coordinates operations through `StudentManagementSystem`
* Performs **application-level input validation**
* Converts domain entities into **immutable Response Models**
* Prevents domain entities from crossing the application boundary

Inbound data enters the system as **DTOs**, which act as safe input contracts.

Outbound results are returned as **immutable Response Models** containing only primitives and immutable collections.

This ensures external layers cannot mutate domain state.

### ⚠️ Architectural Warning — Application Service Gravity

Application services are intentionally designed to be **thin orchestrators**, not containers for business logic.

A common architectural failure in layered systems is the **"Application Service Gravity Problem"**: over time, business rules, validation logic, and workflow decisions begin to accumulate inside application services because they appear to be the "convenient place" to implement new behavior.

When this happens:

* Domain entities become passive data structures
* Business rules leak into orchestration code
* The domain model becomes anemic
* Architectural boundaries erode

To avoid this problem in SMS:

* **Business rules must live exclusively in the domain model**
* Application services may only **coordinate domain behavior**
* Validation performed in the application layer must remain **input-level only**

If a new rule cannot be implemented inside the domain model, this is treated as a **domain modeling problem**, not a reason to move the rule into the application service.

This discipline preserves the integrity of the domain layer and prevents architectural drift as the system evolves.

---

## Infrastructure Layer

The **Infrastructure Layer** implements persistence and external system integrations.

Responsibilities:

* Repository implementations behind domain interfaces
* Storage backends
* Transaction coordination
* Schema initialization and row mapping

Current implementations include:

* **In-memory repositories** for fast testing and prototyping
* **SQLite repositories** with transactional persistence

Both implementations conform to the same repository contracts.

---

## Interfaces / Presentation Layer

The **Presentation Layer** provides external interfaces to the system.

Currently implemented:

* **Command-Line Interface (CLI)**

The CLI acts as a **thin adapter over the application layer**:

* Parses command-line arguments
* Delegates all semantics to application services
* Renders output from immutable response models
* Converts exceptions into user-facing errors and exit codes

The CLI does **not contain business rules or persistence logic**.

---

# 🚀 Features

## Functional Capabilities

* Create and manage students, teachers, and courses
* Assign teachers to courses
* Enroll and drop students from courses
* Assign and remove grades
* Enforce academic rules through domain exceptions

## Architectural Characteristics

* Rich Domain Model enforcing business invariants
* Immutable **Response Models** protecting application boundaries
* Explicit **DTO input contracts**
* Repository-based persistence abstraction
* Multiple interchangeable persistence backends
* Layered validation model
* Production-ready CLI adapter
* Contract-driven architecture verified by automated tests

---

# 🧱 Project Structure

```
StudentManagementSystem/
│
├── application/
│   ├── dtos/            # Application input contracts
│   ├── mappers/         # Domain → response mapping
│   ├── responses/       # Immutable response models
│   ├── validation/      # Application-level validation
│   └── services/        # StudentManagementSystem use-case orchestration
│
├── domain/
│   ├── models/          # Core domain entities
│   ├── repositories/    # Repository interfaces (ports)
│   └── exceptions/      # Domain rule violations
│
├── infrastructure/
│   ├── in_memory/       # In-memory repository implementations
│   └── sqlite/          # SQLite persistence implementation
│
├── cli/                 # Command-Line Interface (presentation layer)
│   ├── rendering/
│   ├── application_adapter.py
│   ├── app_factory.py
│   ├── main.py
│   └── README.md        # CLI contract documentation
│
├── tests/
│   ├── domain/          # Domain unit tests
│   ├── application/     # Application-layer behavior tests
│   ├── infrastructure/  # Infrastructure verification tests
│   ├── integration/     # Cross-layer integration tests
│   ├── system/          # End-to-end system tests
│   └── contracts/       # Repository and architecture contracts
│
├── docs/                # Architecture notes and supporting documentation
│
├── README.md
└── .gitignore
```

---

# 🖥️ Command-Line Interface (CLI)

The project includes a **first-class, production-ready CLI**.

Key properties:

* **Stateless** — each invocation runs in a fresh process
* **Deterministic** — identical inputs produce identical results
* **Scriptable and automation-safe**
* **Exit codes are part of the public API**

The CLI:

* Performs syntax and type-level argument parsing
* Delegates all semantics to the application layer
* Renders output exclusively from immutable response models

The CLI can operate with **multiple persistence backends**, allowing the same interface to run with either in-memory storage or SQLite persistence.

📄 **See [`cli/README.md`](cli/README.md) for full CLI documentation**, including:

* Command reference
* Output model
* Exit-code contract
* Automation examples

---

# ✅ Validation Model

Validation responsibilities are strictly layered:

| Concern                     | Responsible Layer |
| --------------------------- | ----------------- |
| Argument presence / parsing | CLI               |
| Type coercion               | CLI               |
| Semantic input validation   | Application       |
| Business invariants         | Domain            |
| Persistence / state errors  | Repositories      |

This strict separation prevents duplicated logic and ensures consistent error semantics across the system.

---

# 🧪 Testing Strategy

The project uses a **layered testing strategy** aligned with the architecture.

**Domain Tests (`tests/domain`)**

* Verify entity behavior
* Validate domain invariants
* Assert domain exception semantics

**Application Tests (`tests/application`)**

* Verify application-layer validation
* Test response model behavior
* Validate mapping logic

**Infrastructure Tests (`tests/infrastructure`)**

* Verify repository implementations
* Validate schema bootstrapping and persistence behavior

**Integration Tests (`tests/integration`)**

* Validate cross-layer behavior and workflows

**System Tests (`tests/system`)**

* Exercise the full application through the public interface

**Contract Tests (`tests/contracts`)**

* Enforce repository interface contracts
* Ensure backend substitution parity

Together, these tests ensure the system behaves correctly while preserving architectural boundaries.

---

# ▶️ Running the Project

Clone the repository:

```bash
git clone https://github.com/roldesch/student-management-system.git
cd student-management-system
```

Run the full test suite:

```bash
pytest
```

---

# 🔮 Future Enhancements

Possible future extensions include:

* Additional persistence backends (PostgreSQL, NoSQL, etc.)
* REST API layer (FastAPI) reusing existing application services
* JSON output mode for the CLI
* Alternative presentation layers (GUI or TUI)

All new interfaces will reuse the existing **application and domain layers** without modifying core business logic.

---

# 📄 License

This project is open for educational and personal use.
