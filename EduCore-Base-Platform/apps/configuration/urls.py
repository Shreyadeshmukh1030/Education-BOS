from django.urls import path
from . import views

app_name = 'configuration'

urlpatterns = [
    path('', views.setting_list, name='index'),
    path('settings/create/', views.setting_create, name='setting_create'),
    path('settings/edit/<uuid:pk>/', views.setting_edit, name='setting_edit'),
]
