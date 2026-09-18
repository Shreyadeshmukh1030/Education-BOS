from django.db import models
from apps.core.models import BaseModel
from apps.academics.models import SubjectOffering
from apps.people.models import Person

class AssessmentType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Assessment(BaseModel):
    name = models.CharField(max_length=255)
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.SET_NULL, null=True, blank=True)
    subject_offering = models.ForeignKey(SubjectOffering, on_delete=models.CASCADE, related_name='assessments')
    date = models.DateField(null=True, blank=True)
    max_marks = models.DecimalField(max_digits=8, decimal_places=2, default=100.00)
    passing_marks = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.subject_offering.subject.name}"

class Result(BaseModel):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='results')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='assessment_results')
    marks_obtained = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=10, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('assessment', 'person')

    def __str__(self):
        return f"{self.person} - {self.assessment.name} ({self.marks_obtained})"
