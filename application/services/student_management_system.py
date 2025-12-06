# application/services/student_management_system.py

from collections.abc import Iterable

from domain.models.student import Student
from domain.models.teacher import Teacher
from domain.models.course import Course
from domain.repositories.student_repository import StudentRepository
from domain.repositories.teacher_repository import TeacherRepository
from domain.repositories.course_repository import CourseRepository

class StudentManagementSystem:
    """
    Application/service layer.

    Responsibilities:
    - Orchestrates use cases (add entities, enroll, assign, grade, remove).
    - Delegate all invariants to the domain model (Course/Student/Teacher).
    - Depend on repository *interfaces* rather than concrete storage.
      (Dependency Inversion: application ➜ domain abstractions).
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

    # ---------- Create / Read ----------

    def add_student(self, student_id: str, name: str) -> Student:
        """
        Create a new Student and persist it via the StudentRepository.

        Duplicate checking is the responsibility of the repository:
        it should raise DuplicateEntityError if the ID already exists.
        """
        student = Student(student_id, name)
        self.student_repo.add(student)
        return student

    def add_teacher(self, teacher_id: str, name: str) -> Teacher:
        """
        Create a new Teacher and persist it via the TeacherRepository.
        """
        teacher = Teacher(teacher_id, name)
        self.teacher_repo.add(teacher)
        return teacher

    def add_course(self, course_code: str, name: str) -> Course:
        """
        Create a new Course (aggregate root) and persist it via the CourseRepository.
        """
        course = Course(course_code, name)
        self.course_repo.add(course)
        return course

    def get_student(self, student_id: str) -> Student:
        """
        Retrieve an existing Student by ID.

        The repository is responsible for raising EntityNotFoundError
        if the ID does not exist.
        """
        return self.student_repo.get(student_id)

    def get_teacher(self, teacher_id: str) -> Teacher:
        """
        Retrieve an existing Teacher by ID.
        """
        return self.teacher_repo.get(teacher_id)

    def get_course(self, code: str) -> Course:
        """
        Retrieve an existing Course by code.
        """
        return self.course_repo.get(code)

    # Optional convenience query methods

    def list_students(self) -> Iterable[Student]:
        """Return all students as provided by the repository."""
        return self.student_repo.list_all()

    def list_teachers(self) -> Iterable[Teacher]:
        """Return all teachers as provided by the repository."""
        return self.teacher_repo.list_all()

    def list_courses(self) -> Iterable[Course]:
        """Return all courses as provided by the repository."""
        return self.course_repo.list_all()

    # ---------- Delete (with cleanup via aggregate root) ----------
    def remove_course(self, course_code: str) -> None:
        """
        Remove a course from the system.

        Cleanup rules (same as pre-refactor):
        - If the course has a teacher, unassign the teacher.
        - Drop all enrolled students from the course.

        Relationship cleanup is done through the Course aggregate, not by
        mutating Student/Teacher directly.
        """
        course = self.get_course(course_code)

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
        - Drop the student from all courses they are enrolled in via Course.drop.
        """
        student = self.get_student(student_id)

        # Drop this student from all their courses via Course (aggregate root)
        for course in tuple(student.courses):
            course.drop(student)

        self.student_repo.remove(student_id)

    def remove_teacher(self, teacher_id: str) -> None:
        """
        Remove a teacher from the system.

        Cleanup rules:
        - For each course where the teacher is assigned, unassign them via Course.
        """
        teacher = self.get_teacher(teacher_id)

        # Unassign from all courses where this teacher is assigned
        for course in tuple(teacher.courses):
            if course.teacher is teacher:
                course.unassign_teacher()

        self.teacher_repo.remove(teacher_id)

    # ---------- Orchestration of domain operations ----------

    def assign_teacher_to_course(self, teacher_id: str, course_code: str) -> None:
        """
        Assign a teacher to a course.

        Orchestration:
        - Look up Teacher and Course via repositories.
        - Delegate invariants (e.g., "course already has a teacher") to Course.
        """
        teacher = self.get_teacher(teacher_id)
        course = self.get_course(course_code)
        course.assign_teacher(teacher)

    def unassign_teacher_from_course(self, course_code: str) -> None:
        """
        Unassign the teacher from a course (if it is assigned).
        """
        course = self.get_course(course_code)
        course.unassign_teacher()

    def enroll_student_in_course(self, student_id: str, course_code: str) -> None:
        """
        Enroll a student in a course.

        Delegates enrollment rules (duplicate checks, etc.) to Course.
        """
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        course.enroll(student)

    def drop_student_from_course(self, student_id: str, course_code: str) -> None:
        """
        Drop a student from a course.
        Delegates to Course.drop, which guarantees bidirectional cleanup.
        """
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        course.drop(student)

    # ---------- Grades (owned by Student, validated by enrollment) ----------
    def assign_grade_to_student(
            self, student_id: str, course_code: str, value: float
    ) -> None:
        """
        Assign a grade to a student for a given course.

        Invariants are enforced by Student.assign_grade:
        - Student must be enrolled in the course.
        - Grade must be within allowed range.
        """
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        student.assign_grade(course, value)

    def remove_grade_from_student(
            self, student_id: str, course_code: str
    ) -> None:
        """
        Remove an existing grade for a student in a course.
        """
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        student.remove_grade(course)

    def get_student_grade(
            self, student_id: str, course_code: str
    ) -> float | None:
        """
        Retrieve a student's grade for a given course, or None if it is not set.
        """
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        return student.get_grade(course)
