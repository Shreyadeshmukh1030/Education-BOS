from django.db import models
from apps.core.models import BaseModel

class OrganizationType(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Organization(BaseModel):
    name = models.CharField(max_length=255)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True, blank=True)
    logo = models.ImageField(upload_to='organization_logos/', null=True, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    timezone = models.CharField(max_length=100, default='UTC')
    currency = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return self.name

class Campus(BaseModel):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='campuses')
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.organization.name}"

class Department(BaseModel):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')
    head = models.CharField(max_length=255, blank=True, null=True) # Ideally points to a Person, but keep simple for now

    def __str__(self):
        return f"{self.name} - {self.organization.name}"

# We can keep OrganizationSettings integrated into Organization for simplicity as discussed in the plan.
