# application/responses/course_response.py

from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass(frozen=True, slots=True)
class CourseResponse:
    """
    Immutable representation of a course for consumption outside the domain.

    Contains:
    - course_code
    - name
    - teacher_id (None if no teacher assigned)
    - list of student_ids
    """

    course_code: str
    name: str
    teacher_id: Optional[str]
    student_ids: Tuple[str, ...]

    def __init__(
            self,
            *,
            course_code: str,
            name: str,
        teacher_id: Optional[str],
        student_ids: list[str],
    ) -> None:
        object.__setattr__(self, "course_code", course_code)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "teacher_id", teacher_id)
        object.__setattr__(self, "student_ids", tuple(student_ids))