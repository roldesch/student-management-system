# application/mappers/teacher_mapper.py


from application.dtos import TeacherDTO


class TeacherMapper:
    @staticmethod
    def to_dto(teacher) -> TeacherDTO:
        return TeacherDTO(
            teacher_id=teacher.id,
            name=teacher.name,
            course_codes=[course.code for course in teacher.courses],
        )
