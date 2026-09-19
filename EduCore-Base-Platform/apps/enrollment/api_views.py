from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentViewSet(BaseViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
