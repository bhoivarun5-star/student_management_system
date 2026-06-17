from django.contrib import admin
from .models import Student, Department, Course, Enrollment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'credits']
    search_fields = ['code', 'name']
    list_filter = ['department']


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'email', 'department', 'status', 'gpa']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    list_filter = ['status', 'department', 'gender']
    inlines = [EnrollmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'semester', 'grade']
    list_filter = ['semester', 'grade']
