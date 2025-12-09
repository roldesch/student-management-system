# application/dtos/teacher_dto.py

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True, slots=True)
class TeacherDTO:
    """
    Application-level DTO representing a Teacher.

    Fields:
        teacher_id: Stable identity of the teacher.
        name: Display name.
        course_codes: List of course codes where this teacher is assigned.
    """
    teacher_id: str
    name: str
    course_codes: List[str]
