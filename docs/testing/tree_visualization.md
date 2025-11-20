# Test Suite Directory Tree Visualization

This document provides a clear, GitHub-friendly visualization of the test directory structure for the **Student Management System** project.  
It is focused *exclusively* on the test suite and its organization.

---

## 📁 Test Directory Structure

```
tests/
│
├── conftest.py                # Shared fixtures for all tests
│
├── domain/                    # Unit tests for individual domain models
│   ├── test_course.py         # Tests for Course domain rules
│   ├── test_student.py        # Tests for Student domain rules
│   └── test_teacher.py        # Tests for Teacher domain rules
│
├── integration/               # Multi-model interactions (not yet implemented)
│   ├── test_enrollment_flow.py
│   └── test_teacher_assignment_flow.py
│
└── system/                    # Full-system tests for SMS orchestrator
    └── test_student_management_system.py
```

---

## 📘 Notes

- The **domain** folder contains strict domain-rule tests for each model.
- The **integration** folder is designed for scenarios involving multiple models working together.
- The **system** folder will contain orchestrator-level tests for the StudentManagementSystem.
- `conftest.py` provides shared fixtures using narrative, descriptive, factory-style design.

This structure follows professional testing practices seen in modern Python projects.
