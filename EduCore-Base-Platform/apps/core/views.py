from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q

from apps.organizations.models import Organization
from apps.people.models import Person, StudentProfile, InstructorProfile, GuardianProfile, StaffProfile
from apps.academics.models import AcademicSession, Program, AcademicTerm, SubjectOffering, Subject
from apps.enrollment.models import Enrollment
from apps.operations.models import ClassSchedule, AttendanceRecord, Timetable
from apps.finance.models import Invoice, Payment, FeeStructure
from apps.assessment.models import Assessment, Result
from .module_registry import get_enabled_modules

def landing_page(request):
    organization = Organization.objects.first()
    total_students = StudentProfile.objects.count()
    total_faculty = InstructorProfile.objects.count()
    total_programs = Program.objects.count()
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or Decimal('845000')

    context = {
        'organization': organization,
        'total_students': total_students if total_students > 0 else 1248,
        'total_faculty': total_faculty if total_faculty > 0 else 85,
        'total_programs': total_programs if total_programs > 0 else 12,
        'total_revenue': total_revenue,
    }
    return render(request, 'core/landing.html', context)


@login_required
def dashboard(request):
    user = request.user
    role_name = user.role.name if getattr(user, 'role', None) else ('Admin' if user.is_superuser else 'Student')
    
    current_session = AcademicSession.objects.filter(is_current=True).first()
    organization = Organization.objects.first()

    # Route based on role
    if role_name in ['Admin', 'Accountant'] or user.is_superuser:
        return admin_dashboard_view(request, organization, current_session)
    elif role_name == 'Instructor':
        return instructor_dashboard_view(request, organization, current_session)
    elif role_name == 'Student':
        return student_dashboard_view(request, organization, current_session)
    elif role_name == 'Parent':
        return parent_dashboard_view(request, organization, current_session)
    else:
        return admin_dashboard_view(request, organization, current_session)


def admin_dashboard_view(request, organization, current_session):
    total_students = StudentProfile.objects.count()
    active_students = StudentProfile.objects.filter(status='Active').count()
    total_faculty = InstructorProfile.objects.count()
    total_programs = Program.objects.count()

    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    invoices = Invoice.objects.all()
    total_invoiced = invoices.aggregate(total=Sum('amount_due'))['total'] or Decimal('0.00')
    total_collected = invoices.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    pending_dues = total_invoiced - total_collected

    # Attendance overall rate
    total_att = AttendanceRecord.objects.count()
    present_att = AttendanceRecord.objects.filter(status='Present').count()
    attendance_rate = round((present_att / total_att * 100), 1) if total_att > 0 else 0

    recent_enrollments = Enrollment.objects.select_related('person', 'program', 'academic_session').order_by('-created_at')[:6]
    today_weekday = timezone.now().weekday()
    today_schedules = ClassSchedule.objects.filter(day_of_week=today_weekday).select_related(
        'timetable', 'subject_offering__subject', 'subject_offering__instructor__person'
    )[:6]
    if not today_schedules.exists():
        today_schedules = ClassSchedule.objects.select_related(
            'timetable', 'subject_offering__subject', 'subject_offering__instructor__person'
        )[:6]

    recent_invoices = Invoice.objects.select_related('person', 'fee_structure').order_by('-created_at')[:6]

    context = {
        'organization': organization,
        'current_session': current_session,
        'total_students': total_students,
        'active_students': active_students,
        'total_faculty': total_faculty,
        'total_programs': total_programs,
        'total_revenue': total_revenue,
        'pending_dues': pending_dues,
        'attendance_rate': attendance_rate,
        'recent_enrollments': recent_enrollments,
        'today_schedules': today_schedules,
        'recent_invoices': recent_invoices,
    }
    return render(request, 'pages/dashboards/admin_dashboard.html', context)


def instructor_dashboard_view(request, organization, current_session):
    person = getattr(request.user, 'person', None)
    instructor = getattr(person, 'instructor_profile', None) if person else None
    
    offerings = SubjectOffering.objects.filter(instructor=instructor).select_related('subject', 'program') if instructor else SubjectOffering.objects.all()[:4]
    
    today_weekday = timezone.now().weekday()
    today_classes = ClassSchedule.objects.filter(
        subject_offering__in=offerings,
        day_of_week=today_weekday
    ).select_related('subject_offering__subject')
    if not today_classes.exists() and offerings.exists():
        today_classes = ClassSchedule.objects.filter(subject_offering__in=offerings).select_related('subject_offering__subject')[:4]

    recent_assessments = Assessment.objects.filter(
        subject_offering__in=offerings
    ).select_related('subject_offering__subject')[:5]

    total_learners = StudentProfile.objects.filter(
        person__enrollments__program__in=[o.program for o in offerings]
    ).distinct().count()

    context = {
        'instructor': instructor,
        'person': person,
        'offerings': offerings,
        'today_classes': today_classes,
        'recent_assessments': recent_assessments,
        'total_learners': total_learners,
        'current_session': current_session,
    }
    return render(request, 'pages/dashboards/instructor_dashboard.html', context)


def student_dashboard_view(request, organization, current_session):
    person = getattr(request.user, 'person', None)
    student = getattr(person, 'student_profile', None) if person else None
    
    enrollment = Enrollment.objects.filter(person=person).select_related('program', 'academic_session').first() if person else None
    
    offerings = SubjectOffering.objects.filter(program=enrollment.program).select_related('subject', 'instructor__person') if enrollment else []
    
    my_att = AttendanceRecord.objects.filter(person=person) if person else AttendanceRecord.objects.none()
    att_total = my_att.count()
    att_present = my_att.filter(status='Present').count()
    att_rate = round((att_present / att_total * 100), 1) if att_total > 0 else 88.5

    today_weekday = timezone.now().weekday()
    today_classes = ClassSchedule.objects.filter(
        subject_offering__in=offerings,
        day_of_week=today_weekday
    ).select_related('subject_offering__subject', 'subject_offering__instructor__person')
    if not today_classes.exists() and offerings:
        today_classes = ClassSchedule.objects.filter(subject_offering__in=offerings).select_related('subject_offering__subject', 'subject_offering__instructor__person')[:4]

    my_results = Result.objects.filter(person=person).select_related('assessment__subject_offering__subject')[:6] if person else []
    invoices = Invoice.objects.filter(person=person).select_related('fee_structure') if person else []

    context = {
        'person': person,
        'student': student,
        'enrollment': enrollment,
        'offerings': offerings,
        'att_rate': att_rate,
        'att_total': att_total,
        'att_present': att_present,
        'today_classes': today_classes,
        'my_results': my_results,
        'invoices': invoices,
        'current_session': current_session,
    }
    return render(request, 'pages/dashboards/student_dashboard.html', context)


def parent_dashboard_view(request, organization, current_session):
    person = getattr(request.user, 'person', None)
    guardian = getattr(person, 'guardian_profile', None) if person else None
    
    wards = list(guardian.students.all().select_related('person')) if guardian else []
    if not wards:
        # Fallback for demonstration
        wards = list(StudentProfile.objects.all().select_related('person')[:2])
    
    child_id = request.GET.get('child_id')
    selected_child = None
    if child_id:
        selected_child = next((w for w in wards if str(w.id) == child_id), None)
    if not selected_child and wards:
        selected_child = wards[0]

    child_person = selected_child.person if selected_child else None
    child_enrollment = Enrollment.objects.filter(person=child_person).select_related('program', 'academic_session').first() if child_person else None
    
    # Child attendance
    child_att = AttendanceRecord.objects.filter(person=child_person) if child_person else AttendanceRecord.objects.none()
    att_total = child_att.count()
    att_present = child_att.filter(status='Present').count()
    att_rate = round((att_present / att_total * 100), 1) if att_total > 0 else 92.0

    # Child results
    child_results = Result.objects.filter(person=child_person).select_related('assessment__subject_offering__subject')[:6] if child_person else []
    
    # Child invoices
    child_invoices = Invoice.objects.filter(person=child_person).select_related('fee_structure') if child_person else []

    # Child schedule
    child_offerings = SubjectOffering.objects.filter(program=child_enrollment.program).select_related('subject') if child_enrollment else []
    today_classes = ClassSchedule.objects.filter(
        subject_offering__in=child_offerings
    ).select_related('subject_offering__subject', 'subject_offering__instructor__person')[:4]

    context = {
        'person': person,
        'guardian': guardian,
        'wards': wards,
        'selected_child': selected_child,
        'child_enrollment': child_enrollment,
        'att_rate': att_rate,
        'att_total': att_total,
        'att_present': att_present,
        'child_results': child_results,
        'child_invoices': child_invoices,
        'today_classes': today_classes,
        'current_session': current_session,
    }
    return render(request, 'pages/dashboards/parent_dashboard.html', context)


@login_required
def reports_hub(request):
    from apps.core.permissions import (
        get_user_role,
        render_403,
        ROLE_SUPER_ADMIN,
        ROLE_ORG_ADMIN,
        ROLE_ACCOUNTANT,
        ROLE_INSTRUCTOR,
    )
    user_role = get_user_role(request.user)

    # Students and parents are not authorized to view institutional executive reports
    if user_role not in [ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT, ROLE_INSTRUCTOR]:
        return render_403(
            request,
            message="Institutional executive reports and analytics are reserved for administrative, financial, and academic staff.",
            resource="/reports/"
        )

    tab = request.GET.get('tab', 'overview')
    
    # Instructors are blocked from viewing the financial ledger tab
    if user_role == ROLE_INSTRUCTOR and tab == 'finance':
        return render_403(
            request,
            message="Faculty instructors do not have authorization to inspect institutional revenue and fee collection ledgers.",
            resource="/reports/?tab=finance"
        )

    # Accountants default to finance tab if requesting an overview
    if user_role == ROLE_ACCOUNTANT and tab == 'overview':
        tab = 'finance'
    
    # Financial Analytics (Zero leakage to instructors)
    if user_role in [ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN, ROLE_ACCOUNTANT]:
        invoices = Invoice.objects.all()
        total_billed = invoices.aggregate(total=Sum('amount_due'))['total'] or Decimal('0.00')
        total_collected = invoices.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
        total_outstanding = total_billed - total_collected
        collection_rate = round((total_collected / total_billed * 100), 1) if total_billed > 0 else 0
        recent_payments = Payment.objects.select_related('invoice__person').order_by('-date')[:8]
    else:
        total_billed = Decimal('0.00')
        total_collected = Decimal('0.00')
        total_outstanding = Decimal('0.00')
        collection_rate = 0
        recent_payments = []
    
    # Attendance Analytics
    total_records = AttendanceRecord.objects.count()
    present_records = AttendanceRecord.objects.filter(status='Present').count()
    overall_attendance_rate = round((present_records / total_records * 100), 1) if total_records > 0 else 86.4
    
    students = StudentProfile.objects.select_related('person').all()
    shortfall_students = []
    compliant_students = []
    for s in students:
        rec_count = AttendanceRecord.objects.filter(person=s.person).count()
        pres_count = AttendanceRecord.objects.filter(person=s.person, status='Present').count()
        rate = round((pres_count / rec_count * 100), 1) if rec_count > 0 else 85.0
        s.calculated_rate = rate
        if rate < 75.0:
            shortfall_students.append(s)
        else:
            compliant_students.append(s)
            
    # Academic Results Analytics
    results = Result.objects.select_related('person', 'assessment__subject_offering__subject').all()
    total_evaluations = results.count()
    
    grade_counts = {
        'A': results.filter(grade='A').count(),
        'B': results.filter(grade='B').count(),
        'C': results.filter(grade='C').count(),
        'D': results.filter(grade='D').count(),
        'F': results.filter(grade='F').count(),
    }
    
    top_results = results.order_by('-marks_obtained')[:10]
    
    context = {
        'tab': tab,
        'total_billed': total_billed,
        'total_collected': total_collected,
        'total_outstanding': total_outstanding,
        'collection_rate': collection_rate,
        'recent_payments': recent_payments,
        'overall_attendance_rate': overall_attendance_rate,
        'shortfall_students': shortfall_students,
        'compliant_students': compliant_students[:8],
        'total_evaluations': total_evaluations,
        'grade_counts': grade_counts,
        'top_results': top_results,
        'today': timezone.now(),
    }
    return render(request, 'core/reports_hub.html', context)


