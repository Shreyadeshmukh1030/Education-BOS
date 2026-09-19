from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/compose/', views.message_compose, name='message_compose'),
    path('messages/<uuid:pk>/', views.message_detail, name='message_detail'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
