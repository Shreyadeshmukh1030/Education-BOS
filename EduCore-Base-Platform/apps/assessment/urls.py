from django.urls import path
from . import views

app_name = 'assessment'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('assessments/', views.assessment_list, name='assessment_list'),
    path('assessments/create/', views.assessment_create, name='assessment_create'),
    path('assessments/<uuid:pk>/gradebook/', views.assessment_gradebook, name='assessment_gradebook'),
    path('results/', views.result_list, name='result_list'),
    path('assignments/', views.assignments_hub, name='assignment_list'),
    path('assignments/<uuid:pk>/submit/', views.assignment_submit, name='assignment_submit'),
]
