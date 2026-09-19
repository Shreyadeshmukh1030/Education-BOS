from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import Person, StudentProfile, InstructorProfile, StaffProfile, GuardianProfile
from .serializers import (
    PersonSerializer, StudentProfileSerializer, InstructorProfileSerializer,
    StaffProfileSerializer, GuardianProfileSerializer
)

class PersonViewSet(BaseViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class StudentProfileViewSet(BaseViewSet):
    queryset = StudentProfile.objects.all().select_related('person')
    serializer_class = StudentProfileSerializer

class InstructorProfileViewSet(BaseViewSet):
    queryset = InstructorProfile.objects.all().select_related('person')
    serializer_class = InstructorProfileSerializer

class StaffProfileViewSet(BaseViewSet):
    queryset = StaffProfile.objects.all().select_related('person')
    serializer_class = StaffProfileSerializer

class GuardianProfileViewSet(BaseViewSet):
    queryset = GuardianProfile.objects.all().select_related('person')
    serializer_class = GuardianProfileSerializer

# Alias LearnerViewSet to StudentProfileViewSet for backward compatibility if needed by frontend
class LearnerViewSet(StudentProfileViewSet):
    pass
