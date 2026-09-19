from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import Role, User
from .serializers import RoleSerializer, UserSerializer

class RoleViewSet(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
