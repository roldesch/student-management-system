Contributing to StudentManagementSystem

Thank you for your interest in contributing to StudentManagementSystem (SMS).

This project serves as an educational reference implementation of:

Clean Architecture

Domain-Driven Design (DDD)

Repository-based persistence

Layered validation and error taxonomy

All contributions must respect the architectural boundaries described in this document.

1. Architectural Overview

SMS follows Clean Architecture, separating responsibilities into four layers:

Domain Layer       → Business rules and entities
Application Layer  → Use-case orchestration
Infrastructure     → Repository implementations
Presentation       → CLI adapter

Key architectural principles:

Domain models are framework-agnostic

Business rules live only in the domain layer

Application services orchestrate use cases

Infrastructure implements repository interfaces

Presentation layers interact only with application services

Domain entities never cross the application boundary

The canonical project structure is documented in README.md.

2. Branching Strategy

SMS uses a task-focused branching model.

Branch Type Purpose Example
feature/    New capability  feature/sqlite-persistence
bugfix/ Fix defect  bugfix/teacher-assignment
refactor/   Structural improvements refactor/cli-adapter
docs/   Documentation updates   docs/readme-update
ci/ CI/CD changes   ci/pr-review

Guidelines:

Branch from main

Keep branches small and focused

One branch should represent one logical change

Avoid direct commits to main for non-trivial changes

3. Commit Message Conventions

SMS uses Conventional Commits.

Format:

<type>(<scope>): <summary>

<body explaining what and why>

Types:

feat
fix
refactor
docs
test
ci

Common scopes:

domain
application
infrastructure
cli
tests
docs
repo

Examples:

refactor(cli): rename application_api to application_adapter
test(system): add enrollment workflow scenario
docs(readme): update architecture overview
fix(domain): prevent duplicate enrollment

Commit bodies should explain architectural impact when relevant.

4. Code Style and Requirements

General guidelines:

Python 3.10+

Follow PEP8

Avoid unused imports

Avoid code duplication

Keep methods small and cohesive

Architectural constraints:

Domain entities must remain persistence-agnostic

Application services must not depend on infrastructure

Infrastructure modules may depend on domain repository interfaces

Repository implementations must live in the infrastructure layer

Use dependency injection for repository access

Public behavior changes must be covered by tests.

5. Testing Guidelines

The test suite mirrors the architecture.

tests/
├ domain
├ application
├ infrastructure
├ integration
├ system
└ contracts
Domain Tests

tests/domain

Verify entity behavior and invariants

No repositories or application services

Must be deterministic

Application Tests

tests/application

Validate application-layer validation

Verify response model behavior

Test mapping logic

Infrastructure Tests

tests/infrastructure

Validate persistence implementations

Verify schema bootstrapping and row mapping

Integration Tests

tests/integration

Validate multi-layer workflows

Combine domain models and repositories

System Tests

tests/system

Test complete application flows via StudentManagementSystem

Simulate real system usage

Contract Tests

tests/contracts

Enforce repository interface contracts

Ensure backend substitution parity

Test Naming

Use descriptive names:

test_<behavior>_<expected_result>()

Examples:

test_enroll_student_adds_student_to_course
test_assign_grade_to_unenrolled_student_raises_error
6. Pull Request Process

Before opening a PR:

1️⃣ Update your branch

git fetch origin
git rebase origin/main

2️⃣ Run tests

pytest

3️⃣ Validate commit messages follow conventions

4️⃣ Update documentation if needed

PR Content

Every PR should describe:

What changed

Why the change was needed

Architectural impact

Test coverage

Breaking changes (if any)

Example PR title:

refactor(application): introduce repository DI in SMS constructor
7. Architecture Review

Contributions should be reviewed for architectural consistency.

Reviewers should verify:

No Clean Architecture boundary violations

Domain rules remain inside domain entities

Application services remain orchestration-only

Infrastructure does not leak into higher layers

Tests cover new or modified behavior

Automated review workflows may assist this process.

8. Documentation Requirements

Documentation is part of the contribution.

Contributors must update:

README.md when architecture or structure changes

docs/ for architectural explanations

CLI documentation when commands change

Documentation must stay consistent with the actual repository structure.

9. Forbidden Anti-Patterns

The following patterns are not allowed:

Application layer importing infrastructure implementations

Domain entities depending on repositories

Implementing business rules outside the domain layer

Domain entities escaping the application boundary

Skipping tests for behavioral changes

Large commits mixing unrelated changes

10. Thank You

Contributions that follow these guidelines help keep the Student Management System:

maintainable

architecturally consistent

scalable

testable

If you have questions, open a discussion or ask for clarification in your pull request.