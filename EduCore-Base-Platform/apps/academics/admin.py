from django.contrib import admin
from .models import AcademicSession, Program, AcademicTerm, Subject, SubjectOffering

admin.site.register(AcademicSession)
admin.site.register(Program)
admin.site.register(AcademicTerm)
admin.site.register(Subject)
admin.site.register(SubjectOffering)
