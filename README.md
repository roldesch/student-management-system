# Student Management System

A Python-based **Student Management System** built with an object-oriented and domain-driven design approach.  
This project simulates a real academic environment with entities such as **Students**, **Teachers**, and **Courses**, and is architected with clean separation between domain models, application logic, and tests.

---

## 🚀 Features

- Create and manage **students**, **teachers**, and **courses**
- Assign teachers to courses
- Enroll students in courses
- Enforce domain rules through custom exceptions
- Rich-domain entities with protected mutation methods
- Central orchestration through `StudentManagementSystem`
- Manual test suite included

---

## 🧱 Project Structure

```
student-management-system/
│
├── core/
│   ├── admin.py
│   └── student_management_system.py
│
├── exceptions/
│   └── domain_exceptions.py
│
├── models/
│   ├── student.py
│   ├── teacher.py
│   └── course.py
│
├── tests/
│   └── test_system.py
│
├── main.py
├── README.md
└── .gitignore
```

### **Folder Responsibilities**
- **core/** → Application services (orchestration logic), such as `StudentManagementSystem`
- **models/** → Domain entities (`Student`, `Teacher`, `Course`)
- **exceptions/** → Domain-specific exceptions
- **tests/** → Manual and automated tests
- **main.py** → Optional CLI entry point

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

Run the **manual test suite**:

```bash
python tests/test_system.py
```

Or run the main entry point:

```bash
python main.py
```

---

## 🧪 Testing

The `tests/test_system.py` file provides a manual test suite to validate:

- Entity creation
- Assigning teachers
- Enrolling students
- Course relationships
- Domain rule enforcement

Automated tests may be added in future iterations.

## 📂 Test Documentation

A detailed tree visualization of the test suite structure is available here:

👉 [Test Suite Tree Visualization](docs/testing/tree_visualization.md)

---

## 🧩 Domain Model Overview

The system follows a **rich domain model**:

- `Student` manages its own courses  
- `Teacher` manages its assigned courses  
- `Course` maintains its students and teachers  
- All changes are validated and enforced through custom exceptions  

---

## 📚 Future Enhancements

- CLI interface for admin/teacher/student roles  
- JSON persistence layer  
- Reports:  
  - Top-performing students  
  - Course statistics  
  - Enrollment analytics  
- Separation into modules: `infrastructure`, `application`, `domain`  
- Logging and audit trail  

---

## 📄 License

This project is open for educational and personal use.
