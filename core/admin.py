from models.student import Student
from models.teacher import Teacher
from models.course import Course

class Admin:
    def __init__(self):
        self.students = {}  #{id: Student}
        self.teachers = {}  #{id: Teacher}
        self.courses = {}   #{code: Course}

    # --- Helper Lookups ---
    def get_student(self, student_id):
        return self.students.get(student_id)

    def get_teacher(self, teacher_id):
        return self.teachers.get(teacher_id)

    def get_course(self, course_code):
        return self.courses.get(course_code)

    # --- Create Entities ---
    def create_student(self, student_id, name, email):
        if student_id in self.students:
            print("Student already exists!")
            return
        self.students[student_id] = Student(student_id, name, email)

    def create_teacher(self, teacher_id, name, email):
        if teacher_id in self.teachers:
            print("Teacher already exists!")
            return
        self.teachers[teacher_id] = Teacher(teacher_id, name, email)

    def create_course(self, code, name):
        if code in self.courses:
            print("Course already exists!")
            return
        self.courses[code] = Course(code, name)

    # --- Assign Relationships ---
    def enroll_student_to_course(self, student_id, course_code):
        student = self.get_student(student_id)
        course = self.get_course(course_code)

        if student and course:
            course.add_student(student)
        else:
            print("Invalid student or course.")

    def assign_teacher_to_course(self, teacher_id, course_code):
        teacher = self.get_teacher(teacher_id)
        course = self.get_course(course_code)

        if teacher and course:
            course.add_teacher(teacher)
        else:
            print("Invalid teacher or course.")

    # --- Lists ---
    def list_all_students(self):
        for s in self.students.values():
            s.display_info()

    def list_all_teachers(self):
        for t in self.teachers.values():
            t.display_info()

    def list_all_courses(self):
        for c in self.courses.values():
            c.display_info()