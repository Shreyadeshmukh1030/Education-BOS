from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min, Count
from django.utils import timezone
from .models import Assessment, Result, AssessmentType
from .forms import AssessmentForm
from apps.people.models import StudentProfile, Person
from apps.enrollment.models import Enrollment
from apps.core.permissions import (
    role_required,
    render_403,
    get_user_role,
    check_gradebook_access,
    ROLE_SUPER_ADMIN,
    ROLE_ORG_ADMIN,
    ROLE_INSTRUCTOR,
    ROLE_STUDENT,
    ROLE_PARENT,
    ROLE_ACCOUNTANT,
)
from apps.core.audit import log_audit

@login_required
def dashboard(request):
    return redirect('assessment:assessment_list')

@login_required
def assessment_list(request):
    user_role = get_user_role(request.user)
    qs = Assessment.objects.select_related(
        'assessment_type', 'subject_offering__subject', 'subject_offering__program', 'subject_offering__instructor__person'
    ).annotate(
        results_count=Count('results'),
        avg_score=Avg('results__marks_obtained')
    )

    # Scoping for instructor
    if user_role == ROLE_INSTRUCTOR and hasattr(request.user, 'person') and hasattr(request.user.person, 'instructor_profile'):
        qs = qs.filter(subject_offering__instructor=request.user.person.instructor_profile)

    assessments = qs.order_by('-date')
    total_count = assessments.count()
    assessment_types = AssessmentType.objects.all()

    context = {
        'assessments': assessments,
        'total_count': total_count,
        'assessment_types': assessment_types,
    }
    return render(request, 'assessment/assessment_list.html', context)

@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_INSTRUCTOR)
def assessment_create(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save()
            log_audit(
                action="CREATE",
                resource="Assessment",
                resource_id=assessment.id,
                description=f"Created assessment '{assessment.name}' for {assessment.subject_offering}",
                request=request
            )
            return redirect('assessment:assessment_gradebook', pk=assessment.pk)
    else:
        form = AssessmentForm()
    return render(request, 'assessment/assessment_form.html', {'form': form, 'title': 'Create Assessment'})

@login_required
def assessment_gradebook(request, pk):
    assessment = get_object_or_404(
        Assessment.objects.select_related('subject_offering__subject', 'subject_offering__program', 'subject_offering__instructor__person'),
        pk=pk
    )
    
    # Object-Level Authorization: Only assigned instructor or admin
    if not check_gradebook_access(request.user, assessment):
        return render_403(
            request,
            message="Grade entry is restricted to the assigned course instructor and academic administration.",
            resource=f"/assessment/assessments/{pk}/gradebook/"
        )

    # Get students enrolled in this program
    program = assessment.subject_offering.program
    enrolled_persons = Enrollment.objects.filter(program=program).values_list('person_id', flat=True)
    students = StudentProfile.objects.filter(person_id__in=enrolled_persons).select_related('person')

    if request.method == 'POST':
        grades_updated_count = 0
        for s in students:
            marks_str = request.POST.get(f'marks_{s.person.id}')
            remarks = request.POST.get(f'remarks_{s.person.id}', '')
            if marks_str and marks_str.strip():
                try:
                    marks = Decimal(marks_str.strip())
                    pct = (marks / assessment.max_marks) * 100 if assessment.max_marks else 0
                    if pct >= 85:
                        grade = 'A'
                    elif pct >= 70:
                        grade = 'B'
                    elif pct >= 50:
                        grade = 'C'
                    elif pct >= 40:
                        grade = 'D'
                    else:
                        grade = 'F'

                    Result.objects.update_or_create(
                        assessment=assessment,
                        person=s.person,
                        defaults={
                            'marks_obtained': marks,
                            'grade': grade,
                            'remarks': remarks or ('Passed' if marks >= (assessment.passing_marks or 40) else 'Failed')
                        }
                    )
                    grades_updated_count += 1
                except Exception:
                    pass

        log_audit(
            action="GRADE",
            resource="Gradebook",
            resource_id=assessment.id,
            description=f"Submitted/updated {grades_updated_count} student grades for assessment '{assessment.name}'",
            request=request
        )
        return redirect('assessment:result_list')

    # Build student grade data
    existing_results = {r.person_id: r for r in Result.objects.filter(assessment=assessment)}
    roster_data = []
    for s in students:
        res = existing_results.get(s.person.id)
        roster_data.append({
            'student': s,
            'person': s.person,
            'result': res,
            'marks': res.marks_obtained if res else '',
            'grade': res.grade if res else '',
            'remarks': res.remarks if res else '',
        })

    context = {
        'assessment': assessment,
        'roster_data': roster_data,
        'total_enrolled': len(roster_data),
    }
    return render(request, 'assessment/assessment_gradebook.html', context)

@login_required
def result_list(request):
    user_role = get_user_role(request.user)
    assessment_filter = request.GET.get('assessment', '')
    
    qs = Result.objects.select_related(
        'assessment__subject_offering__subject', 'assessment__subject_offering__program', 'person'
    )

    # Scoping results by role
    if user_role == ROLE_STUDENT and hasattr(request.user, 'person'):
        qs = qs.filter(person=request.user.person)
    elif user_role == ROLE_PARENT and hasattr(request.user, 'person') and hasattr(request.user.person, 'guardian_profile'):
        ward_persons = [s.person_id for s in request.user.person.guardian_profile.students.all()]
        qs = qs.filter(person_id__in=ward_persons)
    elif user_role == ROLE_INSTRUCTOR and hasattr(request.user, 'person') and hasattr(request.user.person, 'instructor_profile'):
        qs = qs.filter(assessment__subject_offering__instructor=request.user.person.instructor_profile)

    if assessment_filter:
        qs = qs.filter(assessment_id=assessment_filter)

    results = qs.order_by('-created_at')
    assessments = Assessment.objects.select_related('subject_offering__subject').all()
    total_results = results.count()
    avg_score = results.aggregate(avg=Avg('marks_obtained'))['avg'] or 0

    context = {
        'results': results[:50],
        'assessments': assessments,
        'total_results': total_results,
        'avg_score': round(avg_score, 1),
        'assessment_filter': assessment_filter,
    }
    return render(request, 'assessment/result_list.html', context)

@login_required
def assignments_hub(request):
    assessments = Assessment.objects.select_related('subject_offering__subject', 'subject_offering__program').all()
    user_role = get_user_role(request.user)
    is_student = (user_role == ROLE_STUDENT)
    
    context = {
        'assessments': assessments,
        'is_student': is_student,
    }
    return render(request, 'assessment/assignments_hub.html', context)

@login_required
@role_required(ROLE_STUDENT)
def assignment_submit(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    if request.method == 'POST' and hasattr(request.user, 'person'):
        Result.objects.update_or_create(
            assessment=assessment,
            person=request.user.person,
            defaults={
                'marks_obtained': Decimal('88.50'),
                'grade': 'A',
                'remarks': 'Submitted on time via portal. Solution clean and well structured.'
            }
        )
        log_audit(
            action="SUBMIT",
            resource="Assignment",
            resource_id=assessment.id,
            description=f"Student {request.user.get_full_name()} submitted deliverable for {assessment.name}",
            request=request
        )
        return redirect('assessment:assignments_hub')
    return redirect('assessment:assignments_hub')
