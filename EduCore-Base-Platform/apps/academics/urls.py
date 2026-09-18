from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('programs/', views.program_list, name='program_list'),
    path('programs/create/', views.program_create, name='program_create'),
    path('sessions/', views.session_list, name='session_list'),
    path('subjects/', views.subject_list, name='subject_list'),
]
