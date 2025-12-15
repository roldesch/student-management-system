# application/dtos/course_dto.py

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True, slots=True)
class CourseDTO:
    """
    Application-level DTO representing a Course (aggregate root).

    Fields:
        course_code: Stable identity of the course.
        name: Course name/title.
        teacher_id: ID of the assigned teacher, or None if unassigned.
        student_ids: List of student IDs currently enrolled.
    """
    course_code: str
    name: str
    teacher_id: Optional[str]
    student_ids: List[str]
