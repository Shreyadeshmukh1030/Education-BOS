from django.db import models
from apps.core.models import BaseModel
from apps.organizations.models import Organization
from apps.academics.models import Program, AcademicTerm, SubjectOffering
from apps.people.models import Person

class Timetable(BaseModel):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='timetables')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='timetables')
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, related_name='timetables', null=True, blank=True)
    is_active_timetable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.program.name}"

class ClassSchedule(BaseModel):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='schedules')
    subject_offering = models.ForeignKey(SubjectOffering, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.subject_offering.subject.name} on {self.get_day_of_week_display()} at {self.start_time}"

class AttendanceRecord(BaseModel):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('class_schedule', 'date', 'person')

    def __str__(self):
        return f"{self.person} - {self.date} - {self.status}"
