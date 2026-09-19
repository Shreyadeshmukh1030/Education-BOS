from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import OrganizationType, Organization, Campus, Department
from .serializers import OrganizationTypeSerializer, OrganizationSerializer, CampusSerializer, DepartmentSerializer

class OrganizationTypeViewSet(BaseViewSet):
    queryset = OrganizationType.objects.all()
    serializer_class = OrganizationTypeSerializer


class OrganizationViewSet(BaseViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class CampusViewSet(BaseViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer


class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
