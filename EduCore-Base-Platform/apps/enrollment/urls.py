from django.urls import path
from . import views

app_name = 'enrollment'

urlpatterns = [
    path('', views.enrollment_list, name='index'),
    path('list/', views.enrollment_list, name='enrollment_list'),
    path('create/', views.enrollment_create, name='create'),
    path('<uuid:pk>/', views.enrollment_detail, name='detail'),
]
