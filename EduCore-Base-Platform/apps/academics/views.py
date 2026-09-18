from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AcademicSession, Program, Subject
from .forms import AcademicSessionForm, ProgramForm, SubjectForm

@login_required
def dashboard(request):
    return render(request, 'academics/dashboard.html')

@login_required
def program_list(request):
    programs = Program.objects.filter(is_active=True).select_related('organization')
    return render(request, 'academics/program_list.html', {'programs': programs})

@login_required
def program_create(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academics:program_list')
    else:
        form = ProgramForm()
    return render(request, 'academics/program_form.html', {'form': form, 'title': 'Create Program'})

@login_required
def session_list(request):
    sessions = AcademicSession.objects.filter(is_active=True).select_related('organization')
    return render(request, 'academics/session_list.html', {'sessions': sessions})

@login_required
def subject_list(request):
    subjects = Subject.objects.filter(is_active=True)
    return render(request, 'academics/subject_list.html', {'subjects': subjects})
