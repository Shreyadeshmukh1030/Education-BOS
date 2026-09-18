from django.contrib import admin
from .models import Person, StudentProfile, InstructorProfile, StaffProfile, GuardianProfile

admin.site.register(Person)
admin.site.register(StudentProfile)
admin.site.register(InstructorProfile)
admin.site.register(StaffProfile)
admin.site.register(GuardianProfile)
