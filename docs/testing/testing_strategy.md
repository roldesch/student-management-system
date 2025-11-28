# Testing Strategy for Student Management System

This document describes the testing strategy for the **Student Management System** project.  
It defines the goals, scope, structure, levels, and conventions used in the test suite.

The goal is to ensure the system behaves consistently, follows domain rules, and remains maintainable as the project grows.

---

# 🎯 Objectives of the Test Suite

1. **Validate domain behavior**  
   Ensure each model (Student, Teacher, Course) enforces its domain rules.

2. **Verify interactions across models**  
   Confirm that enrollment, teacher assignment, and course relationships behave correctly.

3. **Ensure system reliability**  
   The StudentManagementSystem orchestrator must correctly manage entities and enforce invariants.

4. **Support refactoring**  
   A clean test suite guarantees that improvements do not break existing behavior.

5. **Provide readable, narrative tests**  
   Test names and fixtures must be descriptive, pronounceable, and explain behavior clearly.

---

# 🧱 Test Suite Structure

The project uses a layered test architecture:

```
tests/
│
├── conftest.py                # Shared fixtures
│
├── domain/                    # Unit tests (model-level)
│   ├── test_course.py
│   ├── test_student.py
│   └── test_teacher.py
│
├── integration/               # Multi-model behavior
│   ├── test_enrollment_flow.py
│   └── test_teacher_assignment_flow.py
│
└── system/                    # System-level SMS tests
    └── test_student_management_system.py
```

---

# 🧪 Levels of Testing

## 1. Domain Tests (`tests/domain/`)
**Purpose:** Validate each domain model in isolation.

These tests assert that:

- Course enforces enrollment rules  
- Student updates its enrolled courses  
- Teacher prevents double assignment  
- Removal methods behave predictably  
- Domain exceptions are raised correctly  

These tests are **highly focused** and use **factory-style fixtures**.

---

## 2. Integration Tests (`tests/integration/`)
**Purpose:** Ensure multiple models behave correctly together.

Examples:

- Enrolling a student through the Course model updates both sides  
- Assigning a teacher reflects in both Teacher and Course  
- Cascading removals maintain consistency  

Integration tests validate *behavioral correctness across multiple entities*.

---

## 3. System Tests (`tests/system/`)
**Purpose:** Validate the full workflow of the StudentManagementSystem orchestrator.

These tests check:

- Adding students/teachers/courses  
- Assigning teachers through the SMS  
- Enrolling/dropping students through the SMS  
- Whether internal registries remain consistent  

They test the **application layer**, not the domain layer.

---

# 🧰 Fixtures and Test Design

## ✔ Fixture Style: *Factory-based*
Fixtures must:

- Be descriptive  
- Produce realistic objects  
- Allow flexible reuse  
- Avoid duplicated setup  
- Use narrative naming (`make_student`, `make_course`, etc.)

Example fixture behavior:

```
student = make_student(id="S01", name="Alice")
course = make_course(code="CS101")
```

---

# 🧠 Naming Conventions

## ✔ Test Names
Test names must follow this format:

```
test_<action>_<condition>_<expected_result>()
```

Examples:

- `test_assigning_teacher_when_course_has_no_teacher_succeeds`
- `test_enrolling_student_already_enrolled_raises_enrollmenterror`

Names should be:

- descriptive  
- readable  
- pronounceable  
- narrative in style  

## ✔ Fixture Names

- `make_student`  
- `make_teacher`  
- `make_course`  
- `make_sms`

Clear and consistent.

---

# 📌 Assertions and Error Handling

The test suite enforces:

- **Exceptions must be raised correctly**
- **State changes must be validated on all sides**
- **Relationships must stay synchronized**
- **Every "success" test has a matching "failure" test**

This ensures a full coverage of both valid and invalid paths.

---

# 🚫 What Tests Should Avoid

- Overuse of mocks (domain should use real objects)  
- Duplicated fixture logic  
- Irrelevant print/debug statements  
- Testing Python built-in behavior  
- Writing overly generalized tests  

Each test must reflect **specific domain rules**, not implementation details.

---

# 🔄 Execution and Workflow

To run all tests:

```bash
pytest -v
```

To run only domain tests:

```bash
pytest tests/domain -v
```

To run a specific test file:

```bash
pytest tests/domain/test_course.py -v
```

---

# 📈 Future Improvements

- Property-based testing for domain invariants  
- Code coverage tracking  
- Performance tests for large enrollments  
- Test fixtures for edge cases (e.g., max capacity)  
- Continuous Integration (CI) pipeline integration  

---

# 🏁 Conclusion

This testing strategy provides a clear, scalable structure for validating the Student Management System.  
It ensures domain correctness, system reliability, and long-term maintainability.

