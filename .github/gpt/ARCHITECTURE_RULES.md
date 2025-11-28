# Architecture Rules for Student Management System (SMS)

## 1. Domain Integrity
- Student, Teacher, and Course enforce all invariants.
- No direct mutation of domain collections.
- Course is the aggregate root for enrollment and teacher assignment.

## 2. Application Layer
- StudentManagementSystem orchestrates domain operations.
- It must never mutate domain internals directly.

## 3. Testing
- Follow testing_strategy.md conventions.
- Every success test must have a failure-path test.
- Fixtures must use the narrative factory style from conftest.py.

## 4. Git Workflow
- Branch names follow feature/bugfix/refactor conventions.
- One commit per behavioral change.
- PRs should be small and focused.
- Commit messages follow <type>(<scope>): <summary> format.

## 5. Clean Architecture
- No infrastructure or UI concerns inside domain.
- Domain entities contain behavior, not just data.
- Avoid anemic domain models.
