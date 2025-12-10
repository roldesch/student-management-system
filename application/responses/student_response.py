# application/responses/student_response.py

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class StudentResponse:
    """
    A read-only application-level representation of a student,
    designed for delivery across the application boundary (CLI/UI/API).

    - Always immutable.
    - Contains only primitive/DTO-safe values (no domain objects).
    - Represents a snapshot of the student state at query time.
    """

    student_id: str
    name: str
    enrolled_courses: List[str]         # list of course codes
    grades: Dict[str, float]            # course_code -> grade
