from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from .models import Student, Department, Course, Enrollment
from .forms import StudentForm, DepartmentForm, CourseForm, EnrollmentForm, StudentSearchForm


# ─── Dashboard ────────────────────────────────────────────────────────────────

def dashboard(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='active').count()
    total_departments = Department.objects.count()
    total_courses = Course.objects.count()

    dept_stats = Department.objects.annotate(student_count=Count('students')).order_by('-student_count')[:5]
    recent_students = Student.objects.select_related('department').order_by('-created_at')[:5]

    status_data = {
        'active': Student.objects.filter(status='active').count(),
        'inactive': Student.objects.filter(status='inactive').count(),
        'graduated': Student.objects.filter(status='graduated').count(),
        'suspended': Student.objects.filter(status='suspended').count(),
    }

    context = {
        'total_students': total_students,
        'active_students': active_students,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'dept_stats': dept_stats,
        'recent_students': recent_students,
        'status_data': status_data,
    }
    return render(request, 'student_app/dashboard.html', context)


# ─── Students ─────────────────────────────────────────────────────────────────

def student_list(request):
    form = StudentSearchForm(request.GET)
    students = Student.objects.select_related('department').all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        department = form.cleaned_data.get('department')
        status = form.cleaned_data.get('status')

        if query:
            students = students.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(student_id__icontains=query) |
                Q(email__icontains=query)
            )
        if department:
            students = students.filter(department=department)
        if status:
            students = students.filter(status=status)

    context = {'students': students, 'form': form, 'total': students.count()}
    return render(request, 'student_app/student_list.html', context)


def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related('department'), pk=pk)
    enrollments = student.enrollments.select_related('course').all()
    context = {'student': student, 'enrollments': enrollments}
    return render(request, 'student_app/student_detail.html', context)


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} created successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'student_app/student_form.html', {'form': form, 'action': 'Add'})


def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student {student.full_name} updated successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_app/student_form.html', {'form': form, 'action': 'Edit', 'student': student})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f'Student {name} deleted successfully.')
        return redirect('student_list')
    return render(request, 'student_app/student_confirm_delete.html', {'student': student})


# ─── Departments ──────────────────────────────────────────────────────────────

def department_list(request):
    departments = Department.objects.annotate(student_count=Count('students'), course_count=Count('courses'))
    return render(request, 'student_app/department_list.html', {'departments': departments})


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f'Department "{dept.name}" created!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'student_app/department_form.html', {'form': form, 'action': 'Add'})


def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department "{dept.name}" updated!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'student_app/department_form.html', {'form': form, 'action': 'Edit', 'department': dept})


def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        name = dept.name
        dept.delete()
        messages.success(request, f'Department "{name}" deleted.')
        return redirect('department_list')
    return render(request, 'student_app/department_confirm_delete.html', {'department': dept})


# ─── Courses ──────────────────────────────────────────────────────────────────

def course_list(request):
    courses = Course.objects.select_related('department').annotate(enrollment_count=Count('enrollments'))
    return render(request, 'student_app/course_list.html', {'courses': courses})


def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course "{course.name}" created!')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'student_app/course_form.html', {'form': form, 'action': 'Add'})


def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course "{course.name}" updated!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'student_app/course_form.html', {'form': form, 'action': 'Edit', 'course': course})


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        name = course.name
        course.delete()
        messages.success(request, f'Course "{name}" deleted.')
        return redirect('course_list')
    return render(request, 'student_app/course_confirm_delete.html', {'course': course})


# ─── Enrollment ───────────────────────────────────────────────────────────────

def enroll_student(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.save()
            messages.success(request, f'Enrolled {student.full_name} in {enrollment.course.name}!')
            return redirect('student_detail', pk=student_pk)
    else:
        form = EnrollmentForm()
    return render(request, 'student_app/enrollment_form.html', {'form': form, 'student': student})
