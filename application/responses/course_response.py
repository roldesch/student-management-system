# application/responses/course_response.py

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
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
    teacher_id: Optional[str]     # may be None
    student_ids: List[str]
