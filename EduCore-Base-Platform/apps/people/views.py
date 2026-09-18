from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Person, StudentProfile
from .forms import PersonForm, StudentProfileForm

@login_required
def people_list(request):
    people = Person.objects.filter(is_active=True)
    return render(request, 'people/people_list.html', {'people': people})

@login_required
def student_list(request):
    students = StudentProfile.objects.filter(is_active=True).select_related('person', 'organization')
    return render(request, 'people/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        student_form = StudentProfileForm(request.POST)
        if person_form.is_valid() and student_form.is_valid():
            person = person_form.save()
            student = student_form.save(commit=False)
            student.person = person
            student.save()
            return redirect('people:detail', pk=person.pk)
    else:
        person_form = PersonForm()
        student_form = StudentProfileForm()
        
    return render(request, 'people/student_form.html', {
        'person_form': person_form,
        'student_form': student_form,
        'title': 'Create Student'
    })

@login_required
def person_detail(request, pk):
    person = get_object_or_404(Person, pk=pk, is_active=True)
    return render(request, 'people/person_detail.html', {'person': person})
