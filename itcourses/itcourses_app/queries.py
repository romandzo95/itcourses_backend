import pandas as pd
from django.db.models import Count, Avg, F
from django.db.models.functions import ExtractMonth

from .models import (
    Student,
    Course,
    Classroom,
    Payment,
    Teacher,
    Enrollment,
    Certificate
)


def get_student_enrollments():
    qs = (
        Student.objects
        .annotate(total_courses=Count("enrollment"))
        .order_by("-total_courses")
        .values("first_name", "last_name", "total_courses")
    )
    return pd.DataFrame(list(qs))


def get_student_avg_grade():
    qs = (
        Student.objects
        .annotate(avg_grade=Avg("certificate__grade"))
        .filter(avg_grade__gt=6.0)
        .order_by("-avg_grade")
        .values("first_name", "last_name", "avg_grade")
    )
    return pd.DataFrame(list(qs))


def get_course_profit():
    qs = (
        Course.objects
        .annotate(total_students=Count("enrollment"))
        .annotate(total_income=F("total_students") * F("price"))
        .order_by("-total_income")
        .values("course_name", "total_students", "total_income")
    )
    return pd.DataFrame(list(qs))


def get_classroom_availability():
    qs = (
        Classroom.objects
        .annotate(lessons_count=Count("schedule"))
        .order_by("-lessons_count")
        .values("room_number", "room_capacity", "lessons_count")
    )
    return pd.DataFrame(list(qs))


def get_payments_by_method():
    qs = (
        Payment.objects
        .values("method")
        .annotate(total=Count("payment_id"))
        .filter(total__gte=2)
        .order_by("-total")
    )
    return pd.DataFrame(list(qs))


def get_courses_for_teacher():
    qs = (
        Teacher.objects
        .annotate(lesson_count=Count("schedule"))
        .filter(specialization__isnull=False)
        .order_by("-lesson_count")
        .values("first_name", "last_name", "specialization", "lesson_count")
    )
    return pd.DataFrame(list(qs))


def get_course_price_stats():
    qs = Course.objects.values("price")
    df = pd.DataFrame(list(qs))

    return {
        "mean_price": df["price"].mean(),
        "median_price": df["price"].median(),
        "min_price": df["price"].min(),
        "max_price": df["price"].max(),
    }


def get_monthly_income():
    qs = (
        Enrollment.objects
        .annotate(
            month=ExtractMonth("enrollment_date"),
            course_price=F("course__price")
        )
        .values("month", "course_price")
    )

    df = pd.DataFrame(list(qs))

    return (
        df.groupby("month")["course_price"]
        .sum()
        .reset_index(name="monthly_income")
    )


def get_avg_grade_by_course():
    qs = (
        Certificate.objects
        .annotate(course_name=F("student__enrollment__course__course_name"))
        .values("course_name", "grade")
    )

    df = pd.DataFrame(list(qs)).dropna()

    return (
        df.groupby("course_name")["grade"]
        .mean()
        .reset_index(name="avg_grade")
    )
