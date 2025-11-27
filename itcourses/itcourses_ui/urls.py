from django.urls import path
from . import views

urlpatterns = [
    path('enrollments/', views.enrollment_list, name="enrollment_list"),
    path('enrollments/<int:pk>/', views.enrollment_detail, name="enrollment_detail"),
    path('enrollments/new/', views.enrollment_create, name="enrollment_create"),
    path('enrollments/<int:pk>/update/', views.enrollment_update, name="enrollment_update"),
    path('enrollments/<int:pk>/delete/', views.enrollment_delete, name="enrollment_delete"),
    path("external/", views.external_list, name="external_list"),
    path("external/delete/<int:pk>/", views.external_author_delete, name="external_author_delete"),
]
