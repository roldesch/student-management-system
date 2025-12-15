# application/mappers/student_mapper.py

from application.dtos import StudentDTO


class StudentMapper:
    @staticmethod
    def to_dto(student) -> StudentDTO:
        return StudentDTO(
            student_id=student.id,
            name=student.name,
            enrolled_courses=[course.code for course in student.courses],
            grades={course.code: student.get_grade(course) for course in student.courses},
        )