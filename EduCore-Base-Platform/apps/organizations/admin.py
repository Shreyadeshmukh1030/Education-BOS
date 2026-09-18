from django.contrib import admin
from .models import OrganizationType, Organization, Campus, Department

admin.site.register(OrganizationType)
admin.site.register(Organization)
admin.site.register(Campus)
admin.site.register(Department)
