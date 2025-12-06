ASCII Architecture Diagram (Clean Architecture + DDD + Repositories)

                     +--------------------------------------+
                     |         Presentation Layer           |
                     |   (CLI / Web API / UI – future)      |
                     +-------------------+------------------+
                                         |
                                         v
                     +--------------------------------------+
                     |          Application Layer           |
                     |  StudentManagementService            |
                     |--------------------------------------|
                     |  - orchestrates use cases            |
                     |  - coordinates domain operations     |
                     |  - interacts ONLY with repository    |
                     |    interfaces                        |
                     +-------------------+------------------+
                                         |
                                         | depends on
                                         v
          +------------------- Repository Interfaces ---------------------+
          |                                                                 |
          |   StudentRepository       TeacherRepository       CourseRepository
          |        (ports)                (ports)                 (ports)
          +----------------------------+------------+-----------------------+
                                         | (DI)
                                         v
                 +-----------------------------------------------------+
                 |                Infrastructure Layer                 |
                 |-----------------------------------------------------|
                 | InMemoryStudentRepository                           |
                 | InMemoryTeacherRepository                           |
                 | InMemoryCourseRepository                            |
                 +----------------------------+------------------------+
                                          ^ implements repositories
                                          |
                          dependency injection via SMS constructor
                                          |
                                          v
         +------------------------------------------------------------------+
         |                         Domain Layer                             |
         |------------------------------------------------------------------|
         |  Entities:   Student, Teacher, Course, Grade                     |
         |  Value Obj:  GradeValue                                         |
         |  Exceptions: EnrollmentError, TeacherAssignmentError, GradeError |
         |                                                                  |
         |  Business rules enforced *here*, independent of infrastructure   |
         |                                                                  |
         +------------------------------------------------------------------+
