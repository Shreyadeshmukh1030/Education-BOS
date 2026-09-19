from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import GlobalSetting
from .serializers import GlobalSettingSerializer

class GlobalSettingViewSet(BaseViewSet):
    queryset = GlobalSetting.objects.all()
    serializer_class = GlobalSettingSerializer
