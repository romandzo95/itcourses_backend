from .views import (
    StudentListCreateView, StudentDetailView,
    TeacherListCreateView, TeacherDetailView,
    CourseListCreateView, CourseDetailView,
    ClassroomListCreateView, ClassroomDetailView,
    EnrollmentListCreateView, EnrollmentDetailView,
    ScheduleListCreateView, ScheduleDetailView,
    PaymentListCreateView, PaymentDetailView,
    CertificateListCreateView, CertificateDetailView,
    ReportView
)
from django.urls import path, include

urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name = 'students-list-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name = 'student-detail'),
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('courses/', CourseListCreateView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('classrooms/', ClassroomListCreateView.as_view(), name='classroom-list'),
    path('classrooms/<int:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('certificates/', CertificateListCreateView.as_view(), name='certificate-list'),
    path('certificates/<int:pk>/', CertificateDetailView.as_view(), name='certificate-detail'),
    path('report/', ReportView.as_view(), name='report'),
]
