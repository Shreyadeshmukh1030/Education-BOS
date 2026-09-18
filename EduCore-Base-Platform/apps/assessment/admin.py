from django.contrib import admin
from .models import AssessmentType, Assessment, Result

admin.site.register(AssessmentType)
admin.site.register(Assessment)
admin.site.register(Result)
