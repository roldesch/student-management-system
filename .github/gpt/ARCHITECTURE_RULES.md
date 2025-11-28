# Architecture Rules for Student Management System (SMS)

## 1. Domain Integrity
- Domain models (Student, Teacher, Course) must enforce all invariants internally.
- No direct mutation of domain collections (e.g., enrollment lists, teacher assignments).
- Course is the aggregate root for enrollment and teacher assignment.
- Entities expose behavior, not setters; invariants must be upheld at all times.

## 2. Application Layer (Use Cases)
- The StudentManagementSystem orchestrates domain operations without leaking domain internals.
- Application services may coordinate entities but never mutate their internal state directly.
- Input/output structures belong here, not in the domain.

## 3. Testing Requirements
- Follow `testing_strategy.md` conventions.
- Every success-path test must be paired with a failure-path test validating invariants or errors.
- Fixtures must use the narrative factory approach from `conftest.py` to ensure readability.
- Domain tests should focus on behavior, not internal implementation details.

## 4. Git & Workflow Standards
- Branch names follow:  
  - `feature/<context>/<description>`  
  - `bugfix/<area>/<issue>`  
  - `refactor/<module>/<goal>`  
  - `docs/<area>`  
  - `ci/<workflow-change>`
- One commit per behavioral or architectural change.
- Pull Requests should be small, cohesive, and easy to review.
- Commit messages follow the `<type>(<scope>): <summary>` format with a clear rationale.

## 5. Clean Architecture Boundaries
- No infrastructure, database, or UI concerns inside the domain layer.
- Domain entities must contain business logic, not serve as anemic data containers.
- Infrastructure implements interfaces defined in the domain or application layer.
- Dependencies always point inward (domain → application → infrastructure).
