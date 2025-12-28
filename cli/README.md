# Student Management System CLI

## Overview

The **Student Management System (SMS) CLI** is a command-line interface for interacting with the Student Management System application.

The CLI is a **thin, stateless presentation adapter** over the application layer. Each invocation runs in a fresh process, making the CLI deterministic, scriptable, and automation-safe.

This document defines the **public CLI contract**.

---

## Architectural Guarantees

The CLI guarantees:

* **Clean Architecture compliance**

  * Depends only on the Application Layer
  * Never accesses domain entities or repositories directly
* **Stateless execution**

  * No shared or persistent process state
  * Each command is independent
* **Stable contracts**

  * Exit codes are part of the public API
  * Output formatting is deterministic

---

## Command Structure

All commands follow the pattern:

```text
sms <resource> <action> [options]
```

Examples:

```bash
sms student add --id S01 --name "Alice"
sms student show S01
sms student list

sms course add --code C01 --name "Math"
sms enroll --student S01 --course C01
```

Each command maps **1:1** to a single application use case.

---

## Resources and Commands

### Student

```bash
sms student add --id <student_id> --name <name>
sms student show <student_id>
sms student list
sms student remove <student_id>
```

### Teacher

```bash
sms teacher add --id <teacher_id> --name <name>
sms teacher show <teacher_id>
sms teacher list
sms teacher remove <teacher_id>
```

### Course

```bash
sms course add --code <course_code> --name <name>
sms course show <course_code>
sms course list
sms course remove <course_code>
```

### Cross-resource operations

```bash
sms enroll --student <student_id> --course <course_code>
sms drop --student <student_id> --course <course_code>

sms assign-teacher --teacher <teacher_id> --course <course_code>
sms unassign-teacher <course_code>
```

### Grades

```bash
sms grade assign --student <student_id> --course <course_code> --value <float>
sms grade remove --student <student_id> --course <course_code>
```

---

## Output Model

* **Query commands** print immutable response snapshots
* **Command-style operations** print:

```text
Success.
```

Output is intended for humans. Scripts should rely on exit codes, not output text.

---

## Exit Codes (Public Contract)

| Code | Meaning                             |
| ---: | ----------------------------------- |
|    0 | Success                             |
|    1 | CLI usage / syntax error            |
|    2 | Application validation error        |
|    3 | Domain rule violation               |
|    4 | State error (not found / duplicate) |
|   10 | System / unexpected error           |

Exit codes are deterministic and stable across versions.

---

## Error Handling

* Errors are classified by type
* Messages are human-facing
* Exit codes are machine-facing

Example:

```bash
sms enroll --student S01 --course C01
# exit code: 3 (domain rule violation)
```

---

## Automation and Scripting

The CLI is designed for automation:

```bash
if ! sms enroll --student S01 --course C01; then
  echo "Enrollment failed"
  exit 1
fi
```

Do not parse output text for control flow.

---

## Versioning Policy

This CLI represents **CLI v1 — Stable Contract**.

From this point forward:

* Changes must be additive
* Output changes are breaking changes
* Exit code changes are breaking changes

---

## License

Internal project documentation.
