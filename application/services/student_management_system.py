# application/services/student_management_system.py

from __future__ import annotations

from typing import Optional

from domain.models.student import Student
from domain.models.teacher import Teacher
from domain.models.course import Course
from domain.repositories.student_repository import StudentRepository
from domain.repositories.teacher_repository import TeacherRepository
from domain.repositories.course_repository import CourseRepository

from application.mappers.student_mapper import StudentMapper
from application.mappers.teacher_mapper import TeacherMapper
from application.mappers.course_mapper import CourseMapper

from application.responses.student_response import StudentResponse
from application.responses.teacher_response import TeacherResponse
from application.responses.course_response import CourseResponse

from application.validation.errors import (
    MissingFieldError,
    EmptyValueError,
    InvalidTypeError,
    InvalidIdentifierError,
)


class StudentManagementSystem:
    """
    Application/service layer.

    Responsibilities:
    - Orchestrates use cases (add entities, enroll, assign, grade, remove).
    - Delegates all invariants to the domain model (Course/Student/Teacher).
    - Depends on repository *interfaces* rather than concrete storage.
      (Dependency Inversion: application ➜ domain abstractions).

    DTO boundary:
    - Domain entities NEVER escape this layer.
    - Public methods return Response Models, primitives, or None.
    """

    def __init__(
            self,
            student_repo: StudentRepository,
            teacher_repo: TeacherRepository,
            course_repo: CourseRepository,
    ) -> None:
        # Injected repository dependencies (ports)
        self.student_repo = student_repo
        self.teacher_repo = teacher_repo
        self.course_repo = course_repo


    # ------------------------------------------------------------------
    # Internal helpers — domain entity access (PRIVATE)
    # ------------------------------------------------------------------

    def _get_student_entity(self, student_id: str) -> Student:
        return self.student_repo.get(student_id)


    def _get_teacher_entity(self, teacher_id: str) -> Teacher:
        return self.teacher_repo.get(teacher_id)


    def _get_course_entity(self, course_code: str) -> Course:
        return self.course_repo.get(course_code)


    # ------------------------------------------------------------------
    # Internal helpers — Domain → DTO → Response (PRIVATE)
    # ------------------------------------------------------------------

    @staticmethod
    def _student_response_from_domain(student: Student) -> StudentResponse:
        dto = StudentMapper.to_dto(student)
        return StudentResponse(
            student_id=dto.student_id,
            name=dto.name,
            enrolled_courses=list(dto.enrolled_courses),
            grades=dict(dto.grades),
        )

    @staticmethod
    def _teacher_response_from_domain(teacher: Teacher) -> TeacherResponse:
        dto = TeacherMapper.to_dto(teacher)
        return TeacherResponse(
            teacher_id=dto.teacher_id,
            name=dto.name,
            course_codes=list(dto.course_codes),
        )

    @staticmethod
    def _course_response_from_domain(course: Course) -> CourseResponse:
        dto = CourseMapper.to_dto(course)
        return CourseResponse(
            course_code=dto.course_code,
            name=dto.name,
            teacher_id=dto.teacher_id,
            student_ids=list(dto.student_ids),
        )


    # ------------------------------------------------------------------
    # Create / Read (PUBLIC — return Response Models)
    # ------------------------------------------------------------------

    def add_student(self, student_id: str, name: str) -> StudentResponse:
        """
        Create a new Student and persist it via the StudentRepository.

        Application-level validation:
            - Validates input shape and semantics
            - Raises structured validation errors
            - Performs no side effects on failure
        """

        # ------------------------------------------------------------
        # student_id validation
        # ------------------------------------------------------------

        if student_id is None:
            raise MissingFieldError(field="student_id")

        if not isinstance(student_id, str):
            raise InvalidTypeError(field="student_id")

        if not student_id.strip():
            # Identifiers are structural, not "empty values"
            raise InvalidIdentifierError(field="student_id")

        # ------------------------------------------------------------
        # name validation
        # ------------------------------------------------------------

        if name is None:
            raise MissingFieldError(field="name")

        if not isinstance(name, str):
            raise InvalidTypeError(field="name")

        if not name.strip():
            raise EmptyValueError(field="name")


        # ------------------------------------------------------------
        # domain construction + persistence (NO validation below)
        # ------------------------------------------------------------

        student = Student(student_id, name)
        self.student_repo.add(student)
        return self._student_response_from_domain(student)


    def add_teacher(self, teacher_id: str, name: str) -> TeacherResponse:
        """
        Create a new Teacher and persist it via the TeacherRepository.

        Application-level validation:
            - Validates input shape and semantics
            - Raises structured validation errors
            - Performs no side effects on failure
        """

        # ------------------------------------------------------------
        # teacher_id validation
        # ------------------------------------------------------------

        if teacher_id is None:
            raise MissingFieldError(field="teacher_id")

        if not isinstance(teacher_id, str):
            raise InvalidTypeError(field="teacher_id")

        if not teacher_id.strip():
            raise InvalidIdentifierError(field="teacher_id")


        # ------------------------------------------------------------
        # name validation
        # ------------------------------------------------------------

        if name is None:
            raise MissingFieldError(field="name")

        if not isinstance(name, str):
            raise InvalidTypeError(field="name")

        if not name.strip():
            raise EmptyValueError(field="name")

        # ------------------------------------------------------------
        # domain construction + persistence (NO validation below)
        # ------------------------------------------------------------

        teacher = Teacher(teacher_id, name)
        self.teacher_repo.add(teacher)
        return self._teacher_response_from_domain(teacher)


    def add_course(self, course_code: str, name: str) -> CourseResponse:
        """
        Create a new Course (aggregate root) and persist it via the CourseRepository.

        Application-level validation:
            - Validates input shape and semantics
            - Raises structured validation errors
            - Performs no side effects on failure
        """

        # ------------------------------------------------------------
        # course_code validation
        # ------------------------------------------------------------

        if course_code is None:
            raise MissingFieldError(field="course_code")

        if not isinstance(course_code, str):
            raise InvalidTypeError(field="course_code")

        if not course_code.strip():
            raise InvalidIdentifierError(field="course_code")


        # ------------------------------------------------------------
        # name validation
        # ------------------------------------------------------------

        if name is None:
            raise MissingFieldError(field="name")

        if not isinstance(name, str):
            raise InvalidTypeError(field="name")

        if not name.strip():
            raise EmptyValueError(field="name")
        

        # ------------------------------------------------------------
        # domain construction + persistence (NO validation below)
        # ------------------------------------------------------------

        course = Course(course_code, name)
        self.course_repo.add(course)
        return self._course_response_from_domain(course)


    def get_student(self, student_id: str) -> StudentResponse:
        """
        Retrieve an existing Student by ID as an immutable snapshot.
        """

        # ------------------------------------------------------------
        # identifier validation
        # ------------------------------------------------------------

        if student_id is None:
            raise MissingFieldError(field="student_id")

        if not isinstance(student_id, str):
            raise InvalidTypeError(field="student_id")

        if not student_id.strip():
            raise InvalidIdentifierError(field="student_id")


        # ------------------------------------------------------------
        # repository access (NO validation below)
        # ------------------------------------------------------------

        student = self._get_student_entity(student_id)
        return self._student_response_from_domain(student)


    def get_teacher(self, teacher_id: str) -> TeacherResponse:
        """
        Retrieve an existing Teacher by ID as an immutable snapshot.
        """

        # ------------------------------------------------------------
        # identifier validation
        # ------------------------------------------------------------

        if teacher_id is None:
            raise MissingFieldError(field="teacher_id")

        if not isinstance(teacher_id, str):
            raise InvalidTypeError(field="teacher_id")

        if not teacher_id.strip():
            raise InvalidIdentifierError(field="teacher_id")


        # ------------------------------------------------------------
        # repository access (NO validation below)
        # ------------------------------------------------------------

        teacher = self._get_teacher_entity(teacher_id)
        return self._teacher_response_from_domain(teacher)

    def get_course(self, code: str) -> CourseResponse:
        """
        Retrieve an existing Course by code as an immutable snapshot.
        """

        # ------------------------------------------------------------
        # identifier validation
        # ------------------------------------------------------------

        if code is None:
            raise MissingFieldError(field="course_code")

        if not isinstance(code, str):
            raise InvalidTypeError(field="course_code")

        if not code.strip():
            raise InvalidIdentifierError(field="course_code")

        # ------------------------------------------------------------
        # repository access (NO validation below)
        # ------------------------------------------------------------

        course = self._get_course_entity(code)
        return self._course_response_from_domain(course)

    # ------------------------------------------------------------------
    # Optional convenience query methods (PUBLIC)
    # ------------------------------------------------------------------

    def list_students(self) -> tuple[StudentResponse, ...]:
        """Return all students as immutable snapshots."""
        return tuple(
            self._student_response_from_domain(s)
            for s in self.student_repo.list_all()
        )

    def list_teachers(self) -> tuple[TeacherResponse, ...]:
        """Return all teachers as immutable snapshots."""
        return tuple(
            self._teacher_response_from_domain(t)
            for t in self.teacher_repo.list_all()
        )

    def list_courses(self) -> tuple[CourseResponse, ...]:
        """Return all courses as immutable snapshots."""
        return tuple(
            self._course_response_from_domain(c)
            for c in self.course_repo.list_all()
        )

    # ------------------------------------------------------------------
    # Delete (with cleanup via aggregate root) — PUBLIC COMMANDS
    # ------------------------------------------------------------------

    def remove_course(self, course_code: str) -> None:
        """
        Remove a course from the system.

        Cleanup rules (same as pre-refactor):
        - If the course has a teacher, unassign the teacher.
        - Drop all enrolled students from the course.

        Relationship cleanup is done through the Course aggregate.
        """
        course = self._get_course_entity(course_code)

        # Unassign teacher if present
        if course.teacher is not None:
            course.unassign_teacher()

        # Drop all enrolled students (iterate over a snapshot to avoid mutating while iterating)
        for student in tuple(course.students):
            course.drop(student)

        # Finally remove from repository
        self.course_repo.remove(course_code)

    def remove_student(self, student_id: str) -> None:
        """
        Remove a student from the system.

        Cleanup rules:
        - Drop the student from all courses they are enrolled in.
        """
        student = self._get_student_entity(student_id)

        # Drop this student from all their courses via Course (aggregate root)
        for course in tuple(student.courses):
            course.drop(student)

        self.student_repo.remove(student_id)

    def remove_teacher(self, teacher_id: str) -> None:
        """
        Remove a teacher from the system.

        Cleanup rules:
        - Unassign the teacher from all courses where they are assigned.
        """
        teacher = self._get_teacher_entity(teacher_id)

        # Unassign from all courses where this teacher is assigned
        for course in tuple(teacher.courses):
            if course.teacher is teacher:
                course.unassign_teacher()

        self.teacher_repo.remove(teacher_id)

    # ------------------------------------------------------------------
    # Orchestration of domain operations — PUBLIC COMMANDS
    # ------------------------------------------------------------------

    def assign_teacher_to_course(self, teacher_id: str, course_code: str) -> None:
        """
        Assign a teacher to a course.

        Invariants are enforced by the Course aggregate.
        """
        teacher = self._get_teacher_entity(teacher_id)
        course = self._get_course_entity(course_code)
        course.assign_teacher(teacher)

    def unassign_teacher_from_course(self, course_code: str) -> None:
        """
        Unassign the teacher from a course (if assigned).
        """
        course = self._get_course_entity(course_code)
        course.unassign_teacher()

    def enroll_student_in_course(self, student_id: str, course_code: str) -> None:
        """
        Enroll a student in a course.

        Enrollment rules are enforced by the Course aggregate.
        """
        student = self._get_student_entity(student_id)
        course = self._get_course_entity(course_code)
        course.enroll(student)

    def drop_student_from_course(self, student_id: str, course_code: str) -> None:
        """
        Drop a student from a course.

        Guarantees bidirectional cleanup via Course.drop.
        """
        student = self._get_student_entity(student_id)
        course = self._get_course_entity(course_code)
        course.drop(student)

    # ------------------------------------------------------------------
    # Grades (owned by Student) — PUBLIC
    # ------------------------------------------------------------------

    def assign_grade_to_student(
            self, student_id: str, course_code: str, value: float
    ) -> None:
        """
        Assign a grade to a student for a given course.

        Invariants are enforced by Student.assign_grade:
        """
        student = self._get_student_entity(student_id)
        course = self._get_course_entity(course_code)
        student.assign_grade(course, value)

    def remove_grade_from_student(
            self, student_id: str, course_code: str
    ) -> None:
        """
        Remove a grade from a student for a given course.
        """
        student = self._get_student_entity(student_id)
        course = self._get_course_entity(course_code)
        student.remove_grade(course)

    def get_student_grade(
            self, student_id: str, course_code: str
    ) -> Optional[float]:
        """
        Retrieve a student's grade for a given course, or None if it is not set.

        This method returns a primitive and is therefore boundary-safe.
        """
        student = self._get_student_entity(student_id)
        course = self._get_course_entity(course_code)
        return student.get_grade(course)
