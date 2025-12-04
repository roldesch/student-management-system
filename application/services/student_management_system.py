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
    - Orchestrates use case (add entities, enroll, assign, grade, remove).
    - Delegate all invariants to the domain model(Course/Student/Teacher).
    - Depend on repository *interfaces* rather than concrete storage.
      (Dependency Inversion: application ➜ domain abstractions).
    """

    def __init__(
            self,
            student_repo: StudentRepository,
            teacher_repo: TeacherRepository,
            course_repo: CourseRepository,
    ) -> None:
        self._students = student_repo
        self._teachers = teacher_repo
        self._courses = course_repo

    # ---------- Create / Read ----------

    def add_student(self, student_id: str, name: str) -> Student:
        """
        Create a new Student and persist it via the StudentRepository.

        Duplicate checking is the responsibility of the repository:
        it should raise DuplicateEntityError if the ID already exists.
        """
        student = Student(student_id, name)
        self._students.add(student)
        return student

    def add_teacher(self, teacher_id: str, name: str) -> Teacher:
        """
        Create a new Teacher and persist it via the TeacherRepository.
        """
        teacher = Teacher(teacher_id, name)
        self._teachers.add(teacher)
        return teacher

    def add_course(self, code: str, name: str) -> Course:
        """
        Create a new Course (aggregate root) and persist it via the CourseRepository.
        """
        course = Course(code, name)
        self._courses.add(course)
        return course

    def get_student(self, student_id: str) -> Student:
        """
        Retrieve an existing Student by ID.

        The repository is responsible for raising EntityNotFoundError
        if the ID does not exist.
        """
        return self._students.get(student_id)

    def get_teacher(self, teacher_id: str) -> Teacher:
        """
        Retrieve an existing Teacher by ID.
        """
        return self._teachers.get(teacher_id)

    def get_course(self, code: str) -> Course:
        """
        Retrieve an existing Course by code.
        """
        return self._courses.get(code)

    # ---------- Delete (with cleanup via aggregate root) ----------
    def remove_course(self, code: str) -> None:
        course = self.get_course(code)

        # Unassign teacher if present
        if course.teacher is not None:
            course.unassign_teacher()

        # Drop all enrolled students (iterate over a snapshot)
        for s in tuple(course.students):
            course.drop(s)

        del self._courses[code]

    def remove_student(self, student_id: str) -> None:
        student = self.get_student(student_id)

        # Drop this student from all their courses via Course
        for c in tuple(student.courses):
            c.drop(student)

        del self._students[student_id]

    def remove_teacher(self, teacher_id: str) -> None:
        teacher = self.get_teacher(teacher_id)

        # Unassign from all courses where this teacher is assigned
        for c in tuple(teacher.courses):
            if c.teacher is teacher:
                c.unassign_teacher()

        del self._teachers[teacher_id]

    # ---------- Orchestration of domain operations ----------
    def assign_teacher_to_course(self, teacher_id: str, course_code: str) -> None:
        teacher = self.get_teacher(teacher_id)
        course = self.get_course(course_code)
        course.assign_teacher(teacher)

    def unassign_teacher_from_course(self, course_code: str) -> None:
        course = self.get_course(course_code)
        course.unassign_teacher()

    def enroll_student_in_course(self, student_id: str, course_code: str) -> None:
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        course.enroll(student)

    def drop_student_from_course(self, student_id: str, course_code: str) -> None:
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        course.drop(student)

    # ---------- Grades (owned by Student, validated by enrollment) ----------
    def assign_grade_to_student(self, student_id: str, course_code: str, value: float) -> None:
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        student.assign_grade(course, value)

    def remove_grade_from_student(self, student_id: str, course_code: str) -> None:
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        student.remove_grade(course)

    def get_student_grade(self, student_id: str, course_code: str) -> float | None:
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        return student.get_grade(course)
