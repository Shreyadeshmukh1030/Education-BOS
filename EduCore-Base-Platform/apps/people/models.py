from django.db import models
from django.conf import settings
from apps.core.models import BaseModel
from apps.organizations.models import Organization, Department

class Person(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='person')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='people_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StudentProfile(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='student_profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='students')
    student_id = models.CharField(max_length=50, unique=True)
    admission_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Active')

    def __str__(self):
        return f"Student: {self.person}"

class InstructorProfile(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='instructor_profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='instructors')
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Instructor: {self.person}"

class StaffProfile(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='staff_profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='staff')
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Staff: {self.person}"

class GuardianProfile(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='guardian_profile')
    relationship = models.CharField(max_length=50)

    def __str__(self):
        return f"Guardian: {self.person}"
