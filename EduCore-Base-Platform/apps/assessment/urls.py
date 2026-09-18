from django.urls import path
from . import views

app_name = 'assessment'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('assessments/', views.assessment_list, name='assessment_list'),
    path('assessments/create/', views.assessment_create, name='assessment_create'),
    path('results/', views.result_list, name='result_list'),
]
