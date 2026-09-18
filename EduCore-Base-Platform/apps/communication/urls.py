from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/compose/', views.message_compose, name='message_compose'),
    path('notifications/', views.notification_list, name='notification_list'),
]
