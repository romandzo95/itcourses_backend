from django.contrib import admin


from django.contrib import admin

from .models import (
    Student, 
    Teacher, 
    Course, 
    Classroom, 
    Enrollment, 
    Schedule, 
    Payment, 
    Certificate
)

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(Enrollment)
admin.site.register(Schedule)
admin.site.register(Payment)
admin.site.register(Certificate)