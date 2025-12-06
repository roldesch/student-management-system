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
│       └── (placeholder for future db-backed repos)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── test_course.py
│   ├── integration/
│   │   ├── __init__.py
│   └── system/
│       ├── __init__.py
│       └── test_student_management_system.py
│
├── .gitignore
├── __init__.py
└── README.md
    







