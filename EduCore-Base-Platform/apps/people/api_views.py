from rest_framework import viewsets
from .models import StudentProfile, InstructorProfile
from .serializers import StudentProfileSerializer

class LearnerViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all().select_related('person')
    serializer_class = StudentProfileSerializer
