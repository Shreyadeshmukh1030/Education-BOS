from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    path('', views.people_list, name='index'),
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('<uuid:pk>/', views.person_detail, name='detail'),
]
