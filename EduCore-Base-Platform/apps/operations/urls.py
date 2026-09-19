from django.urls import path
from . import views

app_name = 'operations'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('timetables/', views.timetable_list, name='timetable_list'),
    path('timetables/create/', views.timetable_create, name='timetable_create'),
    path('timetables/grid/', views.timetable_grid, name='timetable_grid'),
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('attendance/', views.attendance_dashboard, name='attendance_list'),
    path('attendance/dashboard/', views.attendance_dashboard, name='attendance_dashboard'),
    path('attendance/analytics/', views.attendance_analytics, name='attendance_analytics'),
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
]
