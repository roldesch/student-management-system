# application/mappers/__init__.py


from .student_mapper import StudentMapper
from .teacher_mapper import TeacherMapper
from .course_mapper import CourseMapper

__all__ = [
    "StudentMapper",
    "TeacherMapper",
    "CourseMapper",
]
