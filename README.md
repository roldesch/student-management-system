# Student Management System

A Python-based Student Management System (SMS) implemented using Domain-Driven Design (DDD) and Clean Architecture principles.

This project simulates an academic environment involving students, teachers, courses, enrollments, and grades, with a clean separation of concerns between:
- Domain layer (entities and business rules)
- Application layer (use-case orchestration)
- Infrastructure layer (repository implementations)
- Tests (domain, integration, and system levels)

The architecture is fully modular and testable via dependency-injected repositories.

---

## 🚀 Features

- Create and manage students, teachers, and courses
- Assign teachers to courses
- Enroll students in courses
- Assign and retrieve grades
- Enforce domain rules through custom exceptions
- Fully modular architecture (domain → application → infrastructure)
- Repository-based design with dependency injection
- In-memory repository implementations for testing and prototyping
- Automated test suite: domain, integration, system
- Complete Python package structure with __init__.py in all folders

---

## 🧱 Project Structure

StudentManagementSystem/
│
├── .github/
│   ├── gpt/
│   │   ├── ARCHITECTURE_RULES.md
│   │   └── pr_review_prompt.md
│   └── workflows/
│       └── pr-auto-review.yml
│
├── application/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       └── student_management_system.py
│
├── docs/
│   └── testing/
│       ├── testing_strategy.md
│       └── tree_visualization.md
│
├── domain/
│   ├── __init__.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── domain_exceptions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── course.py
│   │   ├── student.py
│   │   └── teacher.py
│   └── repositories/
│       ├── __init__.py
│       ├── base_repository.py
│       ├── course_repository.py
│       ├── student_repository.py
│       └── teacher_repository.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── in_memory/
│   │   ├── __init__.py
│   │   ├── in_memory_course_repository.py
│   │   ├── in_memory_student_repository.py
│   │   └── in_memory_teacher_repository.py
│   └── repositories/
│       ├── __init__.py
│       └── (reserved for future db-backed repos)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── test_course.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── (future integration tests)
│   └── system/
│       ├── __init__.py
│       └── test_student_management_system.py
│
├── .gitignore
├── __init__.py
└── README.md

```

### **Folder Responsibilities**
- application/services/
    Application service layer responsible for orchestrating use cases.
    Contains the core service: StudentManagementSystem.

- domain/models/  
    Domain entities:
       - Student
       - Teacher
       - Course
    These classes enforce business rules and are persistence-agnostic.

- domain/exceptions/  
    Custom domain exceptions enforcing invariants and invalid operations:
        EnrollmentError, TeacherAssignmentError, GradeError, etc.

- domain/repositories/  
    Repository interfaces (ports) specifying how the application layer interacts with persistence.

- infrastructure/in_memory/  
    In-memory repository implementations used for testing and prototyping.

- tests/  
    - domain/ → Pure domain unit tests
    - integration/ → Tests combining repositories and domain behavior
    - system/ → Full end-to-end SMS use-case tests via the application layer

- .github/  
    Automation rules, GPT architectural review materials, and CI workflows.

- docs/testing/  
    Documentation for test strategy and directory visualization.

- .gitignore  
    Excludes virtual environments, IDE files, __pycache__/, test artifacts, etc.

- __init__.py  
    Makes all directories valid Python packages and allows clean import paths.

---

## 📝 Requirements

- Python 3.10+
- (Optional) Virtual environment (`python -m venv .venv`)

---

## ▶️ Running the System

Clone the repository:

```bash
git clone https://github.com/roldesch/student-management-system.git
cd student-management-system
```

Run the test suite:

pytest

Run specific layers:

pytest tests/domain
pytest tests/integration
pytest tests/system

Example: Instantiating the SMS with in-memory repositories

from StudentManagementSystem.application.services import StudentManagementSystem
from StudentManagementSystem.infrastructure.in_memory import (
    InMemoryStudentRepository,
    InMemoryTeacherRepository,
    InMemoryCourseRepository,
)

sms = StudentManagementSystem(
    student_repo=InMemoryStudentRepository(),
    teacher_repo=InMemoryTeacherRepository(),
    course_repo=InMemoryCourseRepository(),
)


---

## 🧪 Testing

The project uses a layered automated test strategy:

- Domain Tests (tests/domain) → Verify entity behavior, invariants, and domain exceptions. 
- Integration Tests (tests/integration) → Validate interactions between repositories and domain logic.
- System Tests (tests/system) → Validate complete SMS use-case flows, including:
- Entity creation
- Teacher assignment
- Student enrollment
- Grade assignment and retrieval
- Relationship cleanup
- The test suite uses dependency injection fixtures via `conftest.py`.

The root conftest.py provides dependency-injected repository fixtures.

All test folders include an __init__.py for proper import resolution.

---

## 🧩 Domain Model Overview

The domain layer is the heart of the system:
- Entities manage their own state and enforce invariants
- Domain exceptions prevent invalid operations
- Domain logic is independent of infrastructure concerns
- Repositories abstract persistence behind interfaces

This ensures high modularity and easy extensibility.  

---

## 📚 Future Enhancements

- Add SQL/NoSQL database-backed repositories
- Introduce a REST API layer (FastAPI)
- Add a CLI frontend
- Implement asynchronous repository variants
- Expand analytics and reporting
- Automated architectural validation in CI

---

## 📄 License

This project is open for educational and personal use.
