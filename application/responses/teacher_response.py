# application/responses/teacher_response.py
"""
    Immutable application-level representation of a teacher.

    Contains only:
    - teacher_id
    - name
    - list of assigned course codes
    """

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True, slots=True)
class TeacherResponse:
    """
        Immutable application-level representation of a teacher.

        Contains only:
        - teacher_id
        - name
        - list of assigned course codes
        """

    teacher_id: str
    name: str
    course_codes: Tuple[str, ...]

    def __init__(
        self,
        *,
        teacher_id: str,
        name: str,
        course_codes: list[str],
    ) -> None:
        object.__setattr__(self, "teacher_id", teacher_id)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "course_codes", tuple(course_codes))