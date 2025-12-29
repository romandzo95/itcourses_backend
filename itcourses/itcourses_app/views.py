from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from .allRepos import allRepos
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Count, Avg, Sum, F
from django.db.models.functions import ExtractMonth
from django.views import View
import pandas as pd

import plotly.io as pio
import plotly.express as px
from django.shortcuts import render
from bokeh.plotting import figure, show

from .parallel_db import benchmark
# Create your views here.

repos = allRepos()

# -------------------- Student --------------------
class StudentListCreateView(APIView):
    def get(self, request):
        students = repos.students.get_all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = repos.students.create(**serializer.validated_data)
            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    def get(self, request, pk):
        try:
            student = repos.students.get_by_id(pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            student = repos.students.update(pk, **request.data)
            if student:
                serializer = StudentSerializer(student)
                return Response(serializer.data)
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        student = repos.students.delete(pk)
        if student:
            return Response({"message": "Student deleted"})
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)


# -------------------- Teacher --------------------
class TeacherListCreateView(APIView):
    def get(self, request):
        teachers = repos.teachers.get_all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            teacher = repos.teachers.create(**serializer.validated_data)
            return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailView(APIView):
    def get(self, request, pk):
        try:
            teacher = repos.teachers.get_by_id(pk)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            teacher = repos.teachers.update(pk, **request.data)
            if teacher:
                serializer = TeacherSerializer(teacher)
                return Response(serializer.data)
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        teacher = repos.teachers.delete(pk)
        if teacher:
            return Response({"message": "Teacher deleted"})
        return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)


# -------------------- Course --------------------
class CourseListCreateView(APIView):
    def get(self, request):
        courses = repos.courses.get_all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = repos.courses.create(**serializer.validated_data)
            return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    def get(self, request, pk):
        try:
            course = repos.courses.get_by_id(pk)
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            course = repos.courses.update(pk, **request.data)
            if course:
                serializer = CourseSerializer(course)
                return Response(serializer.data)
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        course = repos.courses.delete(pk)
        if course:
            return Response({"message": "Course deleted"})
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)


# -------------------- Classroom --------------------
class ClassroomListCreateView(APIView):
    def get(self, request):
        classrooms = repos.classrooms.get_all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            classroom = repos.classrooms.create(**serializer.validated_data)
            return Response(ClassroomSerializer(classroom).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomDetailView(APIView):
    def get(self, request, pk):
        try:
            classroom = repos.classrooms.get_by_id(pk)
            serializer = ClassroomSerializer(classroom)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            classroom = repos.classrooms.update(pk, **request.data)
            if classroom:
                serializer = ClassroomSerializer(classroom)
                return Response(serializer.data)
            return Response({"error": "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        classroom = repos.classrooms.delete(pk)
        if classroom:
            return Response({"message": "Classroom deleted"})
        return Response({"error": "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)


# -------------------- Enrollment --------------------
class EnrollmentListCreateView(APIView):
    def get(self, request):
        enrollments = repos.enrollments.get_all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            enrollment = repos.enrollments.create(**serializer.validated_data)
            return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentDetailView(APIView):
    def get(self, request, pk):
        try:
            enrollment = repos.enrollments.get_by_id(pk)
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            enrollment = repos.enrollments.update(pk, **request.data)
            if enrollment:
                serializer = EnrollmentSerializer(enrollment)
                return Response(serializer.data)
            return Response({"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        enrollment = repos.enrollments.delete(pk)
        if enrollment:
            return Response({"message": "Enrollment deleted"})
        return Response({"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND)


# -------------------- Schedule --------------------
class ScheduleListCreateView(APIView):
    def get(self, request):
        schedules = repos.schedules.get_all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            schedule = repos.schedules.create(**serializer.validated_data)
            return Response(ScheduleSerializer(schedule).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleDetailView(APIView):
    def get(self, request, pk):
        try:
            schedule = repos.schedules.get_by_id(pk)
            serializer = ScheduleSerializer(schedule)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            schedule = repos.schedules.update(pk, **request.data)
            if schedule:
                serializer = ScheduleSerializer(schedule)
                return Response(serializer.data)
            return Response({"error": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        schedule = repos.schedules.delete(pk)
        if schedule:
            return Response({"message": "Schedule deleted"})
        return Response({"error": "Schedule not found"}, status=status.HTTP_404_NOT_FOUND)


# -------------------- Payment --------------------
class PaymentListCreateView(APIView):
    def get(self, request):
        payments = repos.payments.get_all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = repos.payments.create(**serializer.validated_data)
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailView(APIView):
    def get(self, request, pk):
        try:
            payment = repos.payments.get_by_id(pk)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            payment = repos.payments.update(pk, **request.data)
            if payment:
                serializer = PaymentSerializer(payment)
                return Response(serializer.data)
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        payment = repos.payments.delete(pk)
        if payment:
            return Response({"message": "Payment deleted"})
        return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)


# -------------------- Certificate --------------------
class CertificateListCreateView(APIView):
    def get(self, request):
        certificates = repos.certificates.get_all()
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CertificateSerializer(data=request.data)
        if serializer.is_valid():
            certificate = repos.certificates.create(**serializer.validated_data)
            return Response(CertificateSerializer(certificate).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificateDetailView(APIView):
    def get(self, request, pk):
        try:
            certificate = repos.certificates.get_by_id(pk)
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            certificate = repos.certificates.update(pk, **request.data)
            if certificate:
                serializer = CertificateSerializer(certificate)
                return Response(serializer.data)
            return Response({"error": "Certificate not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        certificate = repos.certificates.delete(pk)
        if certificate:
            return Response({"message": "Certificate deleted"})
        return Response({"error": "Certificate not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            certificate = repos.certificates.get_by_id(pk)
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data)
        except:
            return Response({"error": "Certificate not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        certificate = repos.certificates.update(pk, **request.data)
        if certificate:
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data)
        return Response({"error": "Certificate not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        certificate = repos.certificates.delete(pk)
        if certificate:
            return Response({"message": "Certificate deleted"})
        return Response({"error": "Certificate not found"}, status=status.HTTP_404_NOT_FOUND)
    


class ReportView(APIView):
    def get(self, request):
        data = {
            "total_students": Student.objects.count(),
            "total_courses": Course.objects.count(),
            "total_enrollments": Enrollment.objects.count(),
            "average_course_price": Course.objects.aggregate(Avg("price"))["price__avg"],
            "payments_by_method": list(
                Payment.objects.values("method").annotate(total=Count("method"))
            ),
        }
        return Response(data, status=status.HTTP_200_OK)
    


class StudentEnrollments(APIView):
    def get(self, request):
        qs = (
            Student.objects
            .annotate(total_courses=Count("enrollment"))
            .filter(total_courses__gte=0)
            .order_by("-total_courses")
            .values("first_name", "last_name", "total_courses")
        )

        df = pd.DataFrame(list(qs))
        return Response(df.to_dict(orient="records"))
    
class StudentAvgGrade(APIView):
    def get(self, request):
        qs = (
            Student.objects
            .annotate(avg_grade=Avg("certificate__grade"))
            .filter(avg_grade__gt=6.0)
            .order_by("-avg_grade")
            .values("first_name", "last_name", "avg_grade")
        )

        df = pd.DataFrame(list(qs))
        return Response(df.to_dict(orient="records"))
    
class CourseProfit(APIView):
    def get(self, request):
        qs = (
            Course.objects
            .annotate(total_students=Count("enrollment"))
            .annotate(total_income=F("total_students") * F("price"))
            .order_by("-total_income")
            .values("course_name", "total_students", "total_income")
        )

        df = pd.DataFrame(list(qs))
        return Response(df.to_dict(orient="records"))
    

class ClassroomAvailability(APIView):
    def get(self, request):
        qs = (
            Classroom.objects
            .annotate(lessons_count=Count("schedule"))
            .order_by("-lessons_count")
            .values("room_number", "room_capacity", "lessons_count")
        )

        df = pd.DataFrame(list(qs))
        return Response(df.to_dict(orient="records"))
    
class PaymentbyPayMethods(APIView):
    def get(self, request):
        qs = (
            Payment.objects
            .values("method")
            .annotate(total=Count("payment_id"))
            .filter(total__gte=2)
            .order_by("-total")
        )

        df = pd.DataFrame(list(qs))
        return Response(df.to_dict(orient="records"))
    
class CoursesForTeacher(APIView):
    def get(self, request):
        qs = (
            Teacher.objects
            .annotate(lesson_count=Count("schedule"))
            .filter(specialization__isnull=False)
            .order_by("-lesson_count")
            .values("first_name", "last_name", "specialization", "lesson_count")
        )

        df = pd.DataFrame(list(qs))
        return Response(df.to_dict(orient="records"))
    

class CoursePriceStats(APIView):
    def get(self, request):
        qs = Course.objects.all().values("course_id","course_name", "price")

        df = pd.DataFrame(list(qs))

        stats = {
            "mean_price": df["price"].mean(),
            "median_price": df["price"].median(),
            "min_price": df["price"].min(),
            "max_price": df["price"].max()
        }
        return Response(stats)
    
class MonthlyIncome(APIView):
    def get(self, request):
        qs = (
            Enrollment.objects
            .annotate(
                month = ExtractMonth("enrollment_date"),
                course_price = F("course__price")
            )
            .values("month", "course_price")
        )

        df = pd.DataFrame(qs)

        grouped = (
            df.groupby("month")["course_price"]
            .sum()
            .reset_index(name="monthly_income")
        )

        return Response(grouped.to_dict(orient="records"))
    
class AvgGradeByCourse(APIView):
    def get(self, request):
        qs = (
            Certificate.objects
            .annotate(course_name=F("student__enrollment__course__course_name"))
            .values("course_name", "grade")
        )

        df = pd.DataFrame(list(qs)).dropna()

        grouped = (
            df.groupby("course_name")["grade"]
            .mean()
            .reset_index(name="avg_grade")
        )

        return Response(grouped.to_dict(orient="records"))
    


class ParallelBenchmarkAPIView(APIView):
    def get(self, request):
        data = benchmark()
        return Response(data)