from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import AssessmentType, Assessment, Result
from .serializers import AssessmentTypeSerializer, AssessmentSerializer, ResultSerializer

class AssessmentTypeViewSet(BaseViewSet):
    queryset = AssessmentType.objects.all()
    serializer_class = AssessmentTypeSerializer


class AssessmentViewSet(BaseViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer


class ResultViewSet(BaseViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
