from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    path('', views.organization_list, name='index'),
    path('create/', views.organization_create, name='create'),
    path('<uuid:pk>/', views.organization_detail, name='detail'),
]
