from .repositories import (
    StudentRepository,
    TeacherRepository,
    CourseRepository,
    ClassroomRepository,
    EnrollmentRepository,
    ScheduleRepository,
    PaymentRepository,
    CertificateRepository
)

class allRepos:
    def __init__(self):
        self.students = StudentRepository()
        self.teachers = TeacherRepository()
        self.courses = CourseRepository()
        self.classrooms = ClassroomRepository()
        self.enrollments = EnrollmentRepository()
        self.schedules = ScheduleRepository()
        self.payments = PaymentRepository()
        self.certificates = CertificateRepository()


allR = allRepos()
students = allR.students.get_all()