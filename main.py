from core.admin import Admin

def main():
    admin = Admin()

    while True:
        print("\n=== Student Management System ===")
        print("1. Create Student")
        print("2. Create Teacher")
        print("3. Create Course")
        print("4. Enroll Student in Course")
        print("5. Assign Teacher to Course")
        print("6. List All Students")
        print("7. List All Teachers")
        print("8. List All Courses")
        print("9. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            student_id = int(input("Student ID: "))
            name = input("Name: ")
            email = input("Email: ")
            admin.create_student(student_id, name, email)

        elif choice == "2":
            teacher_id = int(input("Teacher ID: "))
            name = input("Name: ")
            email = input("Email: ")
            admin.create_teacher(teacher_id, name, email)

        elif choice == "3":
            code = input("Course Code: ")
            name = input("Course Name: ")
            admin.create_course(code, name)

        elif choice == "4":
            student_id = int(input("Student ID: "))
            course_code = input("Course Code: ")
            admin.enroll_student_to_course(student_id, course_code)

        elif choice == "5":
            teacher_id = int(input("Teacher ID: "))
            course_code = input("Course Code: ")
            admin.assign_teacher_to_course(teacher_id, course_code)

        elif choice == "6":
            admin.list_all_students()

        elif choice == "7":
            admin.list_all_teachers()

        elif choice == "8":
            admin.list_all_courses()

        elif choice == "9":
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
