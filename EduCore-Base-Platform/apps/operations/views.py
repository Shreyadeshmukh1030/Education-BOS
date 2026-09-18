from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Timetable, ClassSchedule, AttendanceRecord
from .forms import TimetableForm, ClassScheduleForm

@login_required
def dashboard(request):
    return render(request, 'operations/dashboard.html')

@login_required
def timetable_list(request):
    timetables = Timetable.objects.filter(is_active=True).select_related('program', 'organization')
    return render(request, 'operations/timetable_list.html', {'timetables': timetables})

@login_required
def timetable_create(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('operations:timetable_list')
    else:
        form = TimetableForm()
    return render(request, 'operations/timetable_form.html', {'form': form, 'title': 'Create Timetable'})

@login_required
def schedule_list(request):
    schedules = ClassSchedule.objects.filter(is_active=True).select_related('timetable', 'subject_offering')
    return render(request, 'operations/schedule_list.html', {'schedules': schedules})

@login_required
def attendance_dashboard(request):
    # A placeholder for complex attendance logic
    return render(request, 'operations/attendance_dashboard.html')
