from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/<int:student_pk>/enroll/', views.enroll_student, name='enroll_student'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),

    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
]
