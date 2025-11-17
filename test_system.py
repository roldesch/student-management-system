# test_system.py
from core.student_management_system import StudentManagementSystem


def run_tests():
    print("\n=== Student Management System: Manual Test Suite ===")

    # Initialize system
    sms = StudentManagementSystem()

    # ---------- Create entities ----------
    print("\n-- Creating students, teachers, and courses --")
    s1 = sms.add_student("S01", "Alice")
    s2 = sms.add_student("S02", "Bob")

    t1 = sms.add_teacher("T01", "Dr. Smith")
    t2 = sms.add_teacher("T02", "Prof. Miller")

    c1 = sms.add_course("CS101", "Intro to Computer Science")
    c2 = sms.add_course("MATH201", "Linear Algebra")

    # ---------- Assign teachers ----------
    print("\n-- Assigning teachers to courses --")
    sms.assign_teacher_to_course("T01", "CS101")
    sms.assign_teacher_to_course("T02", "MATH201")

    # ---------- Enroll students ----------
    print("\n-- Enrolling students --")
    sms.enroll_student_in_course("S01", "CS101")
    sms.enroll_student_in_course("S01", "MATH201")
    sms.enroll_student_in_course("S02", "CS101")

    # ---------- Assign grades ----------
    print("\n-- Assigning grades --")
    sms.assign_grade_to_student("S01", "CS101", 9.0)
    sms.assign_grade_to_student("S02", "CS101", 7.5)

    print(f"Alice's CS101 grade: {sms.get_student_grade('S01', 'CS101')}")
    print(f"Bob's CS101 grade: {sms.get_student_grade('S02', 'CS101')}")

    # ---------- Show data integrity ----------
    print("\n-- Data integrity checks --")
    print(f"CS101 students: {[s.name for s in c1.students]}")
    print(f"CS101 teacher: {c1.teacher.name}")

    print(f"Alice's courses: {[c.code for c in s1.courses]}")
    print(f"Dr. Smith's courses: {[c.code for c in t1.courses]}")

    # ---------- Trigger errors intentionally ----------
    print("\n-- Triggering expected errors --")
    try:
        sms.assign_teacher_to_course("T02", "CS101")  # already has a teacher
    except ValueError as e:
        print("Expected error:", e)

    try:
        sms.enroll_student_in_course("S01", "CS101")  # already enrolled
    except ValueError as e:
        print("Expected error:", e)

    try:
        sms.assign_grade_to_student("S02", "MATH201", 12.0)  # invalid grade
    except ValueError as e:
        print("Expected error:", e)

    # ---------- Cleanup tests ----------
    print("\n-- Removing course and verifying cleanup --")
    sms.remove_course("CS101")

    print(f"Remaining courses: {list(sms._courses.keys())}")
    print(f"Alice's remaining courses: {[c.code for c in s1.courses]}")
    print(f"Dr. Smith's remaining courses: {[c.code for c in t1.courses]}")

    print("\nAll tests completed successfully.\n")


if __name__ == "__main__":
    run_tests()
