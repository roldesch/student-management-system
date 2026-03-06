Student Management System CLI
Overview

The Student Management System (SMS) CLI is a command-line interface for interacting with the Student Management System application.

The CLI is a thin, stateless presentation adapter over the application layer. Each invocation runs in a fresh process, making the CLI deterministic, scriptable, and automation-safe.

The CLI interacts exclusively with application services and response models. It never accesses domain entities, repositories, or infrastructure components directly.

This document defines the public CLI contract.

Architectural Guarantees

The CLI guarantees:

Clean Architecture compliance

Depends only on the Application Layer

Never accesses domain entities or repositories directly

Consumes DTO inputs and renders Response Models

Stateless execution

No shared or persistent process state

Each command is independent

Stable contracts

Exit codes are part of the public API

Output behavior is deterministic

Command semantics remain stable across minor releases

The CLI functions purely as a presentation adapter, delegating all system behavior to the application layer.

Command Structure

Most commands follow the pattern:

sms <resource> <action> [options]

Examples:

sms student add --id S01 --name "Alice"
sms student show S01
sms student list

sms course add --code C01 --name "Math"
sms enroll --student S01 --course C01

Commands generally map 1:1 to a single application use case.

The CLI intentionally exposes both:

resource-oriented operations (student, teacher, course)

domain operations (enrollment, teacher assignment, grading)

This allows the interface to remain aligned with the underlying domain model.

Resources and Commands
Student
sms student add --id <student_id> --name <name>
sms student show <student_id>
sms student list
sms student remove <student_id>
Teacher
sms teacher add --id <teacher_id> --name <name>
sms teacher show <teacher_id>
sms teacher list
sms teacher remove <teacher_id>
Course
sms course add --code <course_code> --name <name>
sms course show <course_code>
sms course list
sms course remove <course_code>
Cross-resource operations
sms enroll --student <student_id> --course <course_code>
sms drop --student <student_id> --course <course_code>

sms assign-teacher --teacher <teacher_id> --course <course_code>
sms unassign-teacher <course_code>
Grades
sms grade assign --student <student_id> --course <course_code> --value <float>
sms grade remove --student <student_id> --course <course_code>
Output Model

Query commands print immutable response snapshots produced by the application layer.

Command-style operations print:

Success.

Output is intended for human readability.
Automation and scripts should rely on exit codes, not output text.

Exit Codes (Public Contract)

Exit codes map directly to architectural error categories.

Code  Meaning
0 Success
1 CLI usage / syntax error
2 Application validation error
3 Domain rule violation
4 State error (not found / duplicate)
10  System / unexpected error

These codes remain stable across versions.

Error Handling

Errors are classified according to the architectural layer where they originate.

CLI errors

Invalid syntax

Missing or malformed arguments

Application errors

Input validation failures

Domain errors

Business rule violations

State errors

Entity not found

Duplicate identity

Errors propagate unchanged from the application and domain layers, preserving their original semantic meaning.

Messages are human-facing.
Exit codes are machine-facing.

Example:

sms enroll --student S01 --course C01
# exit code: 3 (domain rule violation)
Automation and Scripting

The CLI is designed for automation:

if ! sms enroll --student S01 --course C01; then
  echo "Enrollment failed"
  exit 1
fi

Scripts should rely on exit codes for control flow.

Do not parse output text to determine success or failure.

CLI Versioning and Stability

This CLI represents CLI v1 — Stable Contract, starting with SMS version 1.0.0.

The CLI contract is designed to remain stable even as internal architecture evolves.

Stability Guarantees

For all releases within the 1.x.y series:

Command names and hierarchical structure are stable

Required and optional flags retain their meaning

Exit code semantics remain stable and deterministic

Error classification remains consistent

Output semantics remain stable at the meaning level

Formatting may evolve, but the semantic meaning of output fields will not change.

Breaking Changes

The following require a major version bump:

Renaming or removing commands

Changing the meaning of existing flags or arguments

Changing exit code semantics

Reclassifying errors across categories

Changing the semantic meaning of output fields

Allowing domain entities to escape the application boundary

Non-Breaking Changes

The following are backward compatible:

Adding new commands or subcommands

Adding optional flags

Adding infrastructure backends

Performance improvements

Internal refactors preserving observable behavior

This contract ensures that scripts and automation remain reliable across releases.

License

This documentation is part of the Student Management System project.