from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Enrollment
from .forms import EnrollmentForm
from apps.academics.models import Program, AcademicSession

@login_required
def enrollment_list(request):
    status_filter = request.GET.get('status', '').strip()
    program_filter = request.GET.get('program', '').strip()

    enrollments = Enrollment.objects.filter(is_active=True).select_related(
        'person', 'program', 'academic_session', 'organization'
    ).order_by('-created_at')

    if status_filter:
        enrollments = enrollments.filter(status=status_filter)
    if program_filter:
        enrollments = enrollments.filter(program_id=program_filter)

    total_count = Enrollment.objects.count()
    active_count = Enrollment.objects.filter(status='Active').count()
    programs = Program.objects.all()

    context = {
        'enrollments': enrollments,
        'total_count': total_count,
        'active_count': active_count,
        'programs': programs,
        'status_filter': status_filter,
        'program_filter': program_filter,
    }
    return render(request, 'enrollment/enrollment_list.html', context)

@login_required
def enrollment_create(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            return redirect('enrollment:detail', pk=enrollment.pk)
    else:
        form = EnrollmentForm(initial={'status': 'Active'})
    return render(request, 'enrollment/enrollment_form.html', {'form': form, 'title': 'Register New Enrollment'})

@login_required
def enrollment_detail(request, pk):
    enrollment = get_object_or_404(
        Enrollment.objects.select_related('person', 'program', 'academic_session', 'organization'),
        pk=pk, is_active=True
    )
    return render(request, 'enrollment/enrollment_detail.html', {'enrollment': enrollment})
