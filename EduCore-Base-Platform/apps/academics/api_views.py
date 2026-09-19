from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import AcademicSession, Program, AcademicTerm, Subject, SubjectOffering
from .serializers import AcademicSessionSerializer, ProgramSerializer, AcademicTermSerializer, SubjectSerializer, SubjectOfferingSerializer

class AcademicSessionViewSet(BaseViewSet):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer


class ProgramViewSet(BaseViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class AcademicTermViewSet(BaseViewSet):
    queryset = AcademicTerm.objects.all()
    serializer_class = AcademicTermSerializer


class SubjectViewSet(BaseViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectOfferingViewSet(BaseViewSet):
    queryset = SubjectOffering.objects.all()
    serializer_class = SubjectOfferingSerializer
