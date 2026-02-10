# cli/application_api.py

from __future__ import annotations

from typing import Protocol

from application.responses.student_response import StudentResponse
from application.responses.teacher_response import TeacherResponse
from application.responses.course_response import CourseResponse


class StudentManagementSystemAPI(Protocol):
    """
    CLI-owned structural typing contract describing the public use-case
    surface returned by the composition root (create_sms).

    This Protocol MUST exactly mirror the public API of the
    StudentManagementSystem. It introduces no new behavior and
    no new boundary.
    """

    # --- Student use cases ---

    def add_student(self, student_id: str, name: str) -> StudentResponse:
        ...

    def get_student(self, student_id: str) -> StudentResponse:
        ...


    # --- Teacher use cases ---
    def add_teacher(self, teacher_id: str, name: str) -> TeacherResponse:
        ...

    def get_teacher(self, teacher_id: str) -> TeacherResponse:
        ...


    # --- Course use cases ---

    def add_course(self, code: str, name: str) -> CourseResponse:
        ...

    def get_course(self, code: str) -> CourseResponse:
        ...