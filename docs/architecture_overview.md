🏛️ Architecture Overview

The system follows a layered Clean Architecture:

+------------------------------+
|        Presentation          |  ← (not implemented yet)
+------------------------------+
|      Application Layer       |  ← Orchestrates use cases
|   StudentManagementService   |
+------------------------------+
|          Domain              |  ← Entities, logic, invariants
| Students, Teachers, Courses  |
| Exceptions, Value Objects    |
+------------------------------+
|       Infrastructure         |  ← Repository implementations
|  In-memory repositories      |
+------------------------------+