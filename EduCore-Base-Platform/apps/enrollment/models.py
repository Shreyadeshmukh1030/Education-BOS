from django.db import models
from apps.core.models import BaseModel
from apps.people.models import Person
from apps.academics.models import Program, AcademicSession
from apps.organizations.models import Organization

class Enrollment(BaseModel):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Admitted', 'Admitted'),
        ('Enrolled', 'Enrolled'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Dropped', 'Dropped'),
        ('Suspended', 'Suspended'),
    ]

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='enrollments')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='enrollments')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='enrollments')
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')
    
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Enrolled')

    class Meta:
        unique_together = ('person', 'program', 'academic_session')

    def __str__(self):
        return f"{self.person} - {self.program.name} ({self.status})"
