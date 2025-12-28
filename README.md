# Student Management System

A Python-based **Student Management System (SMS)** implemented using **Domain-Driven Design (DDD)** and **Clean Architecture** principles.

The project models an academic environment involving students, teachers, courses, enrollments, and grades, with a strict separation of concerns between architectural layers and clearly defined boundaries between domain logic, application orchestration, and external interfaces.

This repository now represents a **stable, contract-driven system**, including a production-ready CLI.

---

## 🧭 Architecture Overview

The system follows Clean Architecture with explicit responsibilities per layer:

* **Domain Layer**

  * Core entities (`Student`, `Teacher`, `Course`)
  * Business invariants enforced via domain methods and domain-specific exceptions
  * No dependencies on infrastructure or presentation concerns

* **Application Layer**

  * Orchestrates use cases through `StudentManagementSystem`
  * Performs **application-level input validation** (shape, semantics, identifiers)
  * Exposes **immutable Response Models** and DTO-safe data structures
  * Prevents domain entities from crossing application boundaries

* **Infrastructure Layer**

  * Repository implementations (currently in-memory)
  * Implements persistence behind repository interfaces (ports)

* **Interfaces / Presentation Layer**

  * Command-Line Interface (CLI)
  * Acts as a thin adapter over the application layer
  * No business rules, domain logic, or persistence access

---

## 🚀 Features

* Create and manage students, teachers, and courses
* Assign teachers to courses
* Enroll and drop students from courses
* Assign and remove grades
* Enforce business rules through domain exceptions
* Centralized application-level validation
* Immutable application response models
* Repository-based design with dependency injection
* In-memory repositories for testing and prototyping
* Fully automated test suite across all layers
* Production-ready, automation-safe CLI

---

## 🧱 Project Structure

```
StudentManagementSystem/
│
├── application/
│   ├── dtos/            # Application-level DTOs
│   ├── mappers/         # Domain → DTO mapping
│   ├── responses/       # Immutable response models
│   ├── validation/      # Application-level validation errors
│   └── services/        # StudentManagementSystem
│
├── domain/
│   ├── models/          # Core domain entities
│   ├── repositories/    # Repository interfaces (ports)
│   └── exceptions/      # Domain rule violations
│
├── infrastructure/
│   └── in_memory/       # In-memory repository implementations
│
├── cli/                 # Command-Line Interface (presentation layer)
│   ├── commands/
│   ├── rendering/
│   ├── app_factory.py
│   ├── main.py
│   └── README.md        # CLI contract documentation
│
├── tests/
│   ├── domain/          # Domain unit tests
│   ├── integration/     # Cross-layer tests
│   ├── system/          # Application-level system tests
│   └── cli/             # CLI snapshot and subprocess tests
│
├── docs/
│   └── testing/         # Testing strategy and diagrams
│
├── README.md
└── .gitignore
```

---

## 🖥️ Command-Line Interface (CLI)

The project includes a **first-class, production-ready CLI**.

Key properties:

* Stateless: each invocation runs in a fresh process
* Deterministic: identical inputs produce identical observable results
* Scriptable and automation-safe
* Exit codes are part of the public API

The CLI:

* Performs syntax and type-level argument parsing
* Delegates all semantics to the application layer
* Renders output exclusively from immutable response models

📄 **See [`cli/README.md`](cli/README.md) for full CLI documentation**, including:

* Command reference
* Output model
* Exit-code contract
* Automation examples

---

## ✅ Validation Model

Validation responsibilities are strictly layered:

| Concern                     | Responsible Layer |
| --------------------------- | ----------------- |
| Argument presence / parsing | CLI               |
| Type coercion               | CLI               |
| Semantic input validation   | Application       |
| Business invariants         | Domain            |
| Existence / state checks    | Repositories      |

This prevents duplication, leakage, and inconsistent error handling.

---

## 🧪 Testing Strategy

The project uses a layered testing approach:

* **Domain Tests** (`tests/domain`)
  Verify entity behavior, invariants, and domain exceptions.

* **Application / System Tests** (`tests/system`)
  Validate complete use-case flows via the application service.

* **CLI Snapshot Tests**
  Lock output formatting of printers.

* **CLI Subprocess Tests**
  Validate real CLI behavior, exit codes, and error mapping.

Together, these tests guarantee correctness across all architectural boundaries.

---

## ▶️ Running the Project

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

## 🔮 Future Enhancements

* Database-backed repositories (SQL / NoSQL)
* REST API layer (FastAPI) reusing the same application services
* JSON output mode for CLI
* Alternative presentation layers (GUI, TUI)

All future interfaces will reuse the existing application and domain layers.

---

## 📄 License

This project is open for educational and personal use.
