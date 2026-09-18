from django.contrib import admin
from .models import Timetable, ClassSchedule, AttendanceRecord

admin.site.register(Timetable)
admin.site.register(ClassSchedule)
admin.site.register(AttendanceRecord)
