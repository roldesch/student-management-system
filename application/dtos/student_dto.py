# application/dtos/student_dto.py

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass(frozen=True, slots=True)
class StudentDTO:
    """
    Application-level Data Transfer Object representing a Student.

    This is a flattened and serialization-friendly representation:
    - Only primitive / collection types.
    - No references to domain entities.

    Fields:
        student_id: Stable identity of the student.
        name: Display name.
        enrolled_courses: List of course codes the student is enrolled in.
        grades: Mapping of course_code -> grade (float) or None if not graded.
    """
    student_id: str
    name: str
    enrolled_courses: List[str]
    grades: Dict[str, Optional[float]]
