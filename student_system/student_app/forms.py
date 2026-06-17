from django import forms
from .models import Student, Department, Course, Enrollment


class StudentForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'email', 'phone',
            'gender', 'date_of_birth', 'address', 'department', 'status', 'gpa'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. STU001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 8900'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full address'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '4.0', 'placeholder': '0.00 - 4.00'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CS'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'credits', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CS101'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '6'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course', 'semester', 'grade']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Fall 2024'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
        }


class StudentSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by name, ID, or email...'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label='All Departments',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Student.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
