from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Course(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=15, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    credits = models.PositiveIntegerField(default=3)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        ordering = ['code']


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
    ]

    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    courses = models.ManyToManyField(Course, through='Enrollment', blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='student_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['student_id']


class Enrollment(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D', 'D'), ('F', 'F'), ('I', 'Incomplete'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    semester = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.code}"

    class Meta:
        unique_together = ('student', 'course', 'semester')
