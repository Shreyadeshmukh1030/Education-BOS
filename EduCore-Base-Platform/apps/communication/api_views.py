from rest_framework import viewsets
from apps.core.api_views import BaseViewSet
from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer

class MessageViewSet(BaseViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class NotificationViewSet(BaseViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
