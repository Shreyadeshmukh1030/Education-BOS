from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    path('', views.people_list, name='index'),
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('instructors/', views.instructor_list, name='instructor_list'),
    path('guardians/', views.guardian_list, name='guardian_list'),
    path('staff/', views.staff_list, name='staff_list'),
    path('students/<uuid:pk>/', views.person_detail, name='student_detail'),
    path('<uuid:pk>/', views.person_detail, name='detail'),
]
