import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itcourses.settings')
django.setup()


from itcourses_app.allRepos import allRepos

allR = allRepos()

students1 = allR.students


print(students1.get_by_id(1))

print()

print(students1.get_all())

print()

# new_teacher = allR.teachers.create(first_name="Anna", last_name="Ivanova", email="anna@gmail.com", specialization="C++ dev")
# print("New teacher:", new_teacher)

print()

course1 = allR.courses
# new_course = course1.create(course_name = "C++ pro", description="Upper c++ course", duration=3, price=12.9)
# print("New course:", new_course)

print(course1.get_all())


new_course = course1.create(course_name = "Python", description="python basics", duration=4, price=15)
print("New course:", new_course)

print(course1.get_all())

