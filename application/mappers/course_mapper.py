# application/mappers/course_mapper.py


from application.dtos import CourseDTO


class CourseMapper:
    @staticmethod
    def to_dto(course) -> CourseDTO:
        return CourseDTO(
            course_code=course.code,
            name=course.name,
            teacher_id=course.teacher.id if course.teacher else None,
            student_ids=[s.id for s in course.students],
        )
