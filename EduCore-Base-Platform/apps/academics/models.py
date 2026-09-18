from django.db import models
from apps.core.models import BaseModel
from apps.organizations.models import Organization
from apps.people.models import InstructorProfile

class AcademicSession(BaseModel):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='academic_sessions')
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.organization.name}"

class Program(BaseModel):
    name = models.CharField(max_length=255)
    program_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='programs')

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

class AcademicTerm(BaseModel):
    name = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='terms')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.program.name}"

class Subject(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    credits = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class SubjectOffering(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='offerings')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='subject_offerings')
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='subject_offerings')
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_subjects')

    def __str__(self):
        return f"{self.subject.name} - {self.program.name} ({self.academic_session.name})"
