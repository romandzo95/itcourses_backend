from .models import Student, Teacher, Course, Classroom, Enrollment, Certificate, Schedule, Payment

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, obj_id):
        return self.model.objects.get(pk = obj_id)
    
    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)
    

class StudentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Student)

class TeacherRepository(BaseRepository):
    def __init__(self):
        super().__init__(Teacher)

class CourseRepository(BaseRepository):
    def __init__(self):
        super().__init__(Course)

class CertificateRepository(BaseRepository):
    def __init__(self):
        super().__init__(Certificate)

class ScheduleRepository(BaseRepository):
    def __init__(self):
        super().__init__(Schedule)

class PaymentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Payment)
    
class EnrollmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Enrollment)

class ClassroomRepository(BaseRepository):
    def __init__(self):
        super().__init__(Classroom)
    


