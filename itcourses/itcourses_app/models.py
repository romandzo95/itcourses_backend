from django.db import models


class Certificate(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    issue_date = models.DateTimeField()
    grade = models.DecimalField(max_digits=3, decimal_places=1)
    student = models.ForeignKey('Student', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'certificate'

    def __str__(self):
        return f"{self.issue_date} {self.grade} {self.student}"


class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=50)
    room_capacity = models.IntegerField()
    equipment = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classroom'

    def __str__(self):
        return f"{self.room_number} {self.room_capacity} {self.equipment}"


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'course'

    def __str__(self):
        return f"{self.course_name} {self.description} {self.duration} {self.price}"


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    enrollment_date = models.DateField()
    student = models.ForeignKey('Student', models.DO_NOTHING)
    course = models.ForeignKey(Course, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enrollment'

    def __str__(self):
        return f"{self.enrollment_date} {self.student} {self.course}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateTimeField()
    method = models.CharField(max_length=100)
    student = models.ForeignKey('Student', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'payment'

    def __str__(self):
        return f"{self.payment_date} {self.method} {self.student}"


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    course = models.ForeignKey(Course, models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    classroom = models.ForeignKey(Classroom, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'schedule'

    def __str__(self):
        return f"{self.date} {self.time} {self.course} {self.teacher} {self.classroom}"


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=100)
    specialization = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher'

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
