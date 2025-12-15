# application/responses/student_response.py

from dataclasses import dataclass
from types import MappingProxyType
from typing import Tuple, Mapping


@dataclass(frozen=True, slots=True)
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
    enrolled_courses: Tuple[str, ...]
    grades: Mapping[str, float]

    def __init__(
            self,
            *,
            student_id: str,
            name: str,
            enrolled_courses: list[str],
            grades: dict[str, float],
    ) -> None:
        object.__setattr__(self, "student_id", student_id)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "enrolled_courses", tuple(enrolled_courses))
        object.__setattr__(self, "grades", MappingProxyType(dict(grades)))