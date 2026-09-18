from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Enrollment
from .forms import EnrollmentForm

@login_required
def enrollment_list(request):
    enrollments = Enrollment.objects.filter(is_active=True).select_related('person', 'program', 'academic_session', 'organization')
    return render(request, 'enrollment/enrollment_list.html', {'enrollments': enrollments})

@login_required
def enrollment_create(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            return redirect('enrollment:detail', pk=enrollment.pk)
    else:
        form = EnrollmentForm()
    return render(request, 'enrollment/enrollment_form.html', {'form': form, 'title': 'Create Enrollment'})

@login_required
def enrollment_detail(request, pk):
    enrollment = get_object_or_404(Enrollment.objects.select_related('person', 'program', 'academic_session', 'organization'), pk=pk, is_active=True)
    return render(request, 'enrollment/enrollment_detail.html', {'enrollment': enrollment})
