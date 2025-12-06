🧩 CONTRIBUTING.md
Contributing to StudentManagementSystem

Thank you for your interest in contributing to StudentManagementSystem (SMS)!
This project follows Clean Architecture and Domain-Driven Design (DDD) principles, and contributions must align with the architectural and testing standards defined here.

This document explains:

1. Project architecture
2. Branching and workflow strategy
3. Commit message conventions
4. Code style & guidelines
5. Test layers and rules
6. Pull request (PR) expectations
7. Documentation standards
8. Automated architecture review workflow


🏛️ 1. Architectural Overview

The SMS codebase is organized using Clean Architecture, which enforces strict boundaries:

Domain Layer       → Business rules & entities
Application Layer  → Use-case orchestration
Infrastructure     → Repository implementations
Presentation       → (not implemented yet)


Key goals:
- Domain is framework-agnostic
- Application layer depends only on domain abstractions
- Infrastructure depends on domain repository interfaces
- Test layers mirror architectural boundaries
- All directories include __init__.py for packaging consistency
- The full project tree lives in README.md.



🌿 2. Branching Strategy

SMS uses a task-focused branching model:

Branch Type	    Purpose	                         Naming Example
feature/	    New feature or capability	     feature/system-tests
bugfix/	        Fixing a defect	                 bugfix/teacher-assignment
refactor/	    Improving design or structure    refactor/application/di-rewrite
docs/	        Documentation updates	         docs/readme-updates
ci/	            CI/CD or GitHub workflow changes	ci/pr-auto-review

Rules:
- Branch from main unless working in an ongoing refactor.
- Small, focused branches are preferred.
- A branch should represent one logical unit of work.
- Never push directly to main.


📝 3. Commit Message Conventions

SMS uses Conventional Commits with architecture-specific scopes.

Format:

<type>(<scope>): <summary>

<body explaining what and why>

Types:
- feat — new behavior
- fix — bug fix
- refactor — structural code changes
- docs — documentation
- test — test additions/changes
- ci — automation or workflows

Scopes:
- domain, application, infrastructure, system, tests, docs, repo, etc.

Examples:
- refactor(application): inject repositories into SMS constructor
- test(system): add end-to-end enrollment scenario
- docs(readme): update architecture diagram
- fix(domain): prevent double enrollment in the same course

Commit bodies must explain architectural impact.


🧹 4. Code Style & Requirements

- Python 3.10+
- PEP8 formatting
- No unused imports
- Avoid code duplication
- Domain entities must remain persistence-agnostic
- Application services should not import concrete repositories
- Infrastructure modules must only depend on domain repository interfaces
- Use dependency injection for all repository access
- Keep methods cohesive and small
- Public APIs must be covered by tests


🧪 5. Testing Guidelines

The test suite is organized by architectural layer:

tests/
│
├── domain/       → Entity behavior & business rules
├── integration/  → Domain + repository interactions
└── system/       → Full SMS use-case flows

✔ Domain Tests (tests/domain/)
- Test invariants and entity behavior
- No repositories, no application layer
- Should be deterministic and fast

✔ Integration Tests (tests/integration/)
- Use in-memory repositories
- Validate repository interactions with domain models
- No application service calls

✔ System Tests (tests/system/)
- Use the StudentManagementSystem API
- Validate complete business flows:
    * create entities
    * assign teacher
    * enroll student
    * assign grade
    * relationship cleanup
- Always use dependency injection:

sms = StudentManagementSystem(
    student_repo=InMemoryStudentRepository(),
    teacher_repo=InMemoryTeacherRepository(),
    course_repo=InMemoryCourseRepository(),
)

Fixtures
- Defined in tests/conftest.py
- Must return fresh instances
- Should not mutate shared state

Naming conventions
test_<behavior>_<expected_result>()


Examples:
- test_enroll_student_adds_student_to_course
- test_assign_grade_to_unenrolled_student_raises_error

Required:
- Every PR that modifies behavior must modify or add tests.


🔍 6. Pull Request (PR) Process

Before submitting a PR:

✔ 1. Ensure your branch is up to date
- git fetch origin
- git rebase origin/main

✔ 2. Run the full test suite
- pytest

✔ 3. Validate commit messages follow conventions

✔ 4. Confirm all docs relevant to your change are updated

PR Content Requirements
Every PR must include:

- PR Title
- Clear and descriptive, e.g.:
    refactor(application): introduce DI-based repositories
- PR Body
- What changed
- Why the change was needed
- Architectural impact
- Test coverage summary
- Breaking changes, if any



🤖 7. Automated GitHub Architecture Review

This project includes a GPT-based architecture reviewer located in:

.github/gpt/
    ARCHITECTURE_RULES.md
    pr_review_prompt.md


When you submit a PR:
- The pr-auto-review.yml workflow runs automatically
- The GPT reviewer checks for:
    * Clean Architecture boundary violations
    * Missing tests
    * Invalid imports
    * Layer leakage
    * Naming inconsistencies

You must address all review findings before merging.

📚 8. Documentation Requirements
Every contributor must:
- Update relevant docs under docs/
- Update README.md if architecture or public APIs change
- Keep test tree visualization in sync

Documentation is part of the contribution — not optional.

✔ 9. Coding Anti-Patterns (Forbidden)
- Application layer importing concrete infrastructure classes
- Domain models depending on repositories
- Skipping tests for new behavior
- Merging without PR review
- Silent architectural changes
- Massive commits that touch unrelated concerns
- Using mutable default arguments
- Using print debugging inside tests or production code


🎉 10. Thank You!

Contributions following these guidelines will help keep the Student Management System:
- robust
- maintainable
- architecturally consistent
- scalable
- testable

Thank you for helping improve the project!

If you have questions, open a discussion or ask for guidance in your PR.