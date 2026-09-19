from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Person, StudentProfile, InstructorProfile, GuardianProfile, StaffProfile
from .forms import PersonForm, StudentProfileForm
from apps.organizations.models import Organization
from apps.academics.models import Program, SubjectOffering
from apps.enrollment.models import Enrollment
from apps.operations.models import AttendanceRecord, ClassSchedule
from apps.finance.models import Invoice, Payment
from apps.assessment.models import Result
from apps.core.permissions import (
    get_user_role,
    role_required,
    check_student_access,
    get_scoped_students,
    render_403,
    ROLE_SUPER_ADMIN,
    ROLE_ORG_ADMIN,
    ROLE_INSTRUCTOR,
    ROLE_STUDENT,
    ROLE_PARENT,
    ROLE_ACCOUNTANT,
    ROLE_STAFF,
)
from apps.core.audit import log_audit

@login_required
def people_list(request):
    user_role = get_user_role(request.user)
    if user_role == ROLE_STUDENT and hasattr(request.user, 'person'):
        return redirect('people:detail', pk=request.user.person.pk)
    return redirect('people:student_list')


@login_required
def student_list(request):
    user_role = get_user_role(request.user)
    
    # Students are redirected to their own profile - cannot browse other students
    if user_role == ROLE_STUDENT and hasattr(request.user, 'person'):
        return redirect('people:detail', pk=request.user.person.pk)

    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    program_filter = request.GET.get('program', '').strip()

    # Apply Scope-based Queryset filtering
    students = get_scoped_students(request.user).select_related('organization')

    if query:
        students = students.filter(
            Q(person__first_name__icontains=query) |
            Q(person__last_name__icontains=query) |
            Q(person__email__icontains=query) |
            Q(student_id__icontains=query)
        )

    if status_filter:
        students = students.filter(status=status_filter)

    student_data = []
    for s in students:
        enrollment = Enrollment.objects.filter(person=s.person).select_related('program').first()
        if program_filter and enrollment and str(enrollment.program.id) != program_filter:
            continue
            
        att_records = AttendanceRecord.objects.filter(person=s.person)
        total_att = att_records.count()
        present_att = att_records.filter(status='Present').count()
        att_pct = round((present_att / total_att * 100), 1) if total_att > 0 else 90.0

        # Instructors do NOT see invoice balances
        invoice = None
        if user_role in [ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT, ROLE_PARENT]:
            invoice = Invoice.objects.filter(person=s.person).first()

        student_data.append({
            'profile': s,
            'person': s.person,
            'enrollment': enrollment,
            'attendance_rate': att_pct,
            'invoice': invoice,
        })

    programs = Program.objects.all()

    context = {
        'students': student_data,
        'query': query,
        'status_filter': status_filter,
        'program_filter': program_filter,
        'programs': programs,
        'total_count': len(student_data),
    }
    return render(request, 'people/student_list.html', context)


@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_STAFF)
def student_create(request):
    org = Organization.objects.first()
    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES)
        student_form = StudentProfileForm(request.POST)
        if person_form.is_valid() and student_form.is_valid():
            person = person_form.save()
            student = student_form.save(commit=False)
            student.person = person
            if not student.organization_id and org:
                student.organization = org
            student.save()
            
            # Audit log
            log_audit(
                action="CREATE",
                resource="StudentProfile",
                resource_id=student.id,
                description=f"Created student {person.first_name} {person.last_name} ({student.student_id})",
                request=request
            )
            return redirect('people:detail', pk=person.pk)
    else:
        person_form = PersonForm()
        student_form = StudentProfileForm(initial={'organization': org, 'status': 'Active'})
        
    return render(request, 'people/student_form.html', {
        'person_form': person_form,
        'student_form': student_form,
        'title': 'Admit New Student'
    })


@login_required
def person_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)
    user_role = get_user_role(request.user)

    # Object-Level Authorization Check
    if not check_student_access(request.user, person):
        return render_403(
            request,
            message="You are not authorized to inspect this candidate profile. It is outside your designated academic scope.",
            resource=f"/people/students/{person.pk}/"
        )

    active_tab = request.GET.get('tab', 'overview')

    student_profile = getattr(person, 'student_profile', None)
    instructor_profile = getattr(person, 'instructor_profile', None)
    guardian_profile = getattr(person, 'guardian_profile', None)

    enrollments = Enrollment.objects.filter(person=person).select_related('program', 'academic_session')
    attendance_records = AttendanceRecord.objects.filter(person=person).select_related('class_schedule__subject_offering__subject').order_by('-date')[:20]
    total_att = AttendanceRecord.objects.filter(person=person).count()
    present_att = AttendanceRecord.objects.filter(person=person, status='Present').count()
    att_rate = round((present_att / total_att * 100), 1) if total_att > 0 else 90.0

    # Prevent financial data leakage to Instructors
    invoices = []
    if user_role in [ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT, ROLE_STUDENT, ROLE_PARENT]:
        invoices = Invoice.objects.filter(person=person).select_related('fee_structure').order_by('-created_at')

    results = Result.objects.filter(person=person).select_related('assessment__subject_offering__subject')

    guardians = person.student_profile.guardians.all().select_related('person') if student_profile else []
    taught_offerings = SubjectOffering.objects.filter(instructor=instructor_profile).select_related('subject', 'program') if instructor_profile else []

    context = {
        'person': person,
        'student_profile': student_profile,
        'instructor_profile': instructor_profile,
        'guardian_profile': guardian_profile,
        'active_tab': active_tab,
        'enrollments': enrollments,
        'attendance_records': attendance_records,
        'attendance_rate': att_rate,
        'total_attendance': total_att,
        'present_attendance': present_att,
        'invoices': invoices,
        'results': results,
        'guardians': guardians,
        'taught_offerings': taught_offerings,
    }
    return render(request, 'people/person_detail.html', context)


@login_required
def instructor_list(request):
    query = request.GET.get('q', '').strip()
    instructors = InstructorProfile.objects.select_related('person', 'department', 'organization').all()
    if query:
        instructors = instructors.filter(
            Q(person__first_name__icontains=query) |
            Q(person__last_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(department__name__icontains=query)
        )

    instructor_data = []
    for inst in instructors:
        offerings = SubjectOffering.objects.filter(instructor=inst).select_related('subject')
        instructor_data.append({
            'profile': inst,
            'person': inst.person,
            'offerings': offerings,
        })

    return render(request, 'people/instructor_list.html', {
        'instructors': instructor_data,
        'query': query,
    })


@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT, ROLE_STAFF)
def guardian_list(request):
    guardians = GuardianProfile.objects.select_related('person').all()
    guardian_data = []
    for g in guardians:
        wards = g.students.all().select_related('person')
        guardian_data.append({
            'profile': g,
            'person': g.person,
            'wards': wards,
        })
    return render(request, 'people/guardian_list.html', {'guardians': guardian_data})


@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_STAFF)
def staff_list(request):
    staff = StaffProfile.objects.select_related('person', 'department').all()
    return render(request, 'people/staff_list.html', {'staff': staff})
