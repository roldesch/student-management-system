# application/responses/teacher_response.py

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
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
    course_codes: List[str]
