from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assessment, Result
from .forms import AssessmentForm

@login_required
def dashboard(request):
    return render(request, 'assessment/dashboard.html')

@login_required
def assessment_list(request):
    assessments = Assessment.objects.filter(is_active=True).select_related('assessment_type', 'subject_offering')
    return render(request, 'assessment/assessment_list.html', {'assessments': assessments})

@login_required
def assessment_create(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assessment:assessment_list')
    else:
        form = AssessmentForm()
    return render(request, 'assessment/assessment_form.html', {'form': form, 'title': 'Create Assessment'})

@login_required
def result_list(request):
    results = Result.objects.filter(is_active=True).select_related('assessment', 'person')
    return render(request, 'assessment/result_list.html', {'results': results})
