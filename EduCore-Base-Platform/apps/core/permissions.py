from functools import wraps
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.db.models import Q

# 1. Canonical Roles
ROLE_SUPER_ADMIN = 'SUPER_ADMIN'
ROLE_ORG_ADMIN = 'ORG_ADMIN'
ROLE_INSTRUCTOR = 'INSTRUCTOR'
ROLE_STUDENT = 'STUDENT'
ROLE_PARENT = 'PARENT'
ROLE_ACCOUNTANT = 'ACCOUNTANT'
ROLE_STAFF = 'STAFF'

ALL_ROLES = [
    ROLE_SUPER_ADMIN,
    ROLE_ORG_ADMIN,
    ROLE_INSTRUCTOR,
    ROLE_STUDENT,
    ROLE_PARENT,
    ROLE_ACCOUNTANT,
    ROLE_STAFF,
]

ADMIN_ROLES = [ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN]


def get_user_role(user):
    """
    Returns the normalized role string for the authenticated user.
    """
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return ROLE_SUPER_ADMIN

    role_obj = getattr(user, 'role', None)
    if not role_obj:
        if user.is_staff:
            return ROLE_ORG_ADMIN
        return ROLE_STUDENT

    role_name = (role_obj.name or '').strip().lower()
    if 'super' in role_name:
        return ROLE_SUPER_ADMIN
    elif 'admin' in role_name:
        return ROLE_ORG_ADMIN
    elif 'instructor' in role_name or 'faculty' in role_name or 'teacher' in role_name:
        return ROLE_INSTRUCTOR
    elif 'student' in role_name:
        return ROLE_STUDENT
    elif 'parent' in role_name or 'guardian' in role_name:
        return ROLE_PARENT
    elif 'accountant' in role_name or 'finance' in role_name:
        return ROLE_ACCOUNTANT
    elif 'staff' in role_name:
        return ROLE_STAFF

    return ROLE_STUDENT


def render_403(request, message=None, resource=None):
    """
    Renders a unified branded 403 Access Restricted page.
    """
    context = {
        'error_message': message or 'You do not have permission to access this resource.',
        'resource': resource or request.path,
        'user_role': get_user_role(request.user),
    }
    return render(request, '403.html', context, status=403)


# 2. View Decorators
def role_required(*allowed_roles):
    """
    Enforces that the logged-in user has one of the allowed roles.
    Rejects with a custom 403 page if unauthorized.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())

            user_role = get_user_role(request.user)
            # Super Admin has universal access
            if user_role == ROLE_SUPER_ADMIN or user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            return render_403(
                request,
                message=f"Your current role ({user_role}) does not have permission to access this module.",
                resource=request.path
            )
        return _wrapped_view
    return decorator


# 3. Object-Level Authorization Helpers
def check_student_access(user, student_or_person):
    """
    Validates whether the user is authorized to view or manage this specific student's record.
    """
    user_role = get_user_role(user)
    if user_role in ADMIN_ROLES or user_role == ROLE_ACCOUNTANT:
        return True

    from apps.people.models import Person, StudentProfile
    
    # Determine the target Person
    target_person = student_or_person if isinstance(student_or_person, Person) else getattr(student_or_person, 'person', None)
    if not target_person:
        return False

    # Student viewing self
    user_person = getattr(user, 'person', None)
    if not user_person:
        return False

    if user_role == ROLE_STUDENT:
        return target_person.id == user_person.id

    # Parent viewing linked ward
    if user_role == ROLE_PARENT:
        guardian_profile = getattr(user_person, 'guardian_profile', None)
        if not guardian_profile:
            return False
        return guardian_profile.students.filter(person=target_person).exists()

    # Instructor viewing assigned student
    if user_role == ROLE_INSTRUCTOR:
        inst_profile = getattr(user_person, 'instructor_profile', None)
        if not inst_profile:
            return False
        from apps.enrollment.models import Enrollment
        from apps.academics.models import SubjectOffering
        # Check if student is enrolled in any offering taught by this instructor
        instructor_programs = SubjectOffering.objects.filter(instructor=inst_profile).values_list('program_id', flat=True)
        return Enrollment.objects.filter(person=target_person, program_id__in=instructor_programs).exists()

    return False


def check_invoice_access(user, invoice):
    """
    Validates whether the user is authorized to view or settle this specific fee invoice.
    """
    user_role = get_user_role(user)
    if user_role in ADMIN_ROLES or user_role == ROLE_ACCOUNTANT:
        return True

    user_person = getattr(user, 'person', None)
    if not user_person:
        return False

    # Student owns invoice
    if user_role == ROLE_STUDENT:
        return invoice.person_id == user_person.id

    # Parent owns linked child's invoice
    if user_role == ROLE_PARENT:
        guardian_profile = getattr(user_person, 'guardian_profile', None)
        if not guardian_profile:
            return False
        return guardian_profile.students.filter(person=invoice.person).exists()

    # Instructors have zero invoice access
    return False


def check_gradebook_access(user, assessment):
    """
    Validates whether the user can enter or modify grades for this assessment.
    Only the assigned instructor or an admin may modify marks.
    """
    user_role = get_user_role(user)
    if user_role in ADMIN_ROLES:
        return True

    if user_role == ROLE_INSTRUCTOR:
        user_person = getattr(user, 'person', None)
        if not user_person:
            return False
        inst_profile = getattr(user_person, 'instructor_profile', None)
        if not inst_profile:
            return False
        # Check if assessment subject offering belongs to this instructor
        return assessment.subject_offering.instructor_id == inst_profile.id

    return False


# 4. Scoped Queryset Helpers
def get_scoped_students(user):
    """
    Returns StudentProfile queryset scoped to user's permitted visibility.
    """
    from apps.people.models import StudentProfile
    user_role = get_user_role(user)

    if user_role in ADMIN_ROLES or user_role == ROLE_ACCOUNTANT:
        return StudentProfile.objects.filter(is_active=True).select_related('person')

    user_person = getattr(user, 'person', None)
    if not user_person:
        return StudentProfile.objects.none()

    if user_role == ROLE_STUDENT:
        return StudentProfile.objects.filter(person=user_person, is_active=True)

    if user_role == ROLE_PARENT:
        guardian_profile = getattr(user_person, 'guardian_profile', None)
        if not guardian_profile:
            return StudentProfile.objects.none()
        return guardian_profile.students.filter(is_active=True).select_related('person')

    if user_role == ROLE_INSTRUCTOR:
        inst_profile = getattr(user_person, 'instructor_profile', None)
        if not inst_profile:
            return StudentProfile.objects.none()
        from apps.academics.models import SubjectOffering
        from apps.enrollment.models import Enrollment
        programs = SubjectOffering.objects.filter(instructor=inst_profile).values_list('program_id', flat=True)
        enrolled_person_ids = Enrollment.objects.filter(program_id__in=programs).values_list('person_id', flat=True)
        return StudentProfile.objects.filter(person_id__in=enrolled_person_ids, is_active=True).select_related('person')

    return StudentProfile.objects.none()


def get_scoped_invoices(user):
    """
    Returns Invoice queryset scoped to user's permitted visibility.
    Instructors receive an empty queryset (no financial leakage).
    """
    from apps.finance.models import Invoice
    user_role = get_user_role(user)

    if user_role in ADMIN_ROLES or user_role == ROLE_ACCOUNTANT:
        return Invoice.objects.filter(is_active=True).select_related('person', 'fee_structure')

    user_person = getattr(user, 'person', None)
    if not user_person:
        return Invoice.objects.none()

    if user_role == ROLE_STUDENT:
        return Invoice.objects.filter(person=user_person, is_active=True).select_related('fee_structure')

    if user_role == ROLE_PARENT:
        guardian_profile = getattr(user_person, 'guardian_profile', None)
        if not guardian_profile:
            return Invoice.objects.none()
        wards_persons = [s.person_id for s in guardian_profile.students.all()]
        return Invoice.objects.filter(person_id__in=wards_persons, is_active=True).select_related('person', 'fee_structure')

    # Instructors and other staff have zero access
    return Invoice.objects.none()


def get_scoped_payments(user):
    """
    Returns Payment queryset scoped to user's permitted visibility.
    """
    from apps.finance.models import Payment
    user_role = get_user_role(user)

    if user_role in ADMIN_ROLES or user_role == ROLE_ACCOUNTANT:
        return Payment.objects.filter(is_active=True).select_related('invoice__person')

    user_person = getattr(user, 'person', None)
    if not user_person:
        return Payment.objects.none()

    if user_role == ROLE_STUDENT:
        return Payment.objects.filter(invoice__person=user_person, is_active=True).select_related('invoice')

    if user_role == ROLE_PARENT:
        guardian_profile = getattr(user_person, 'guardian_profile', None)
        if not guardian_profile:
            return Payment.objects.none()
        wards_persons = [s.person_id for s in guardian_profile.students.all()]
        return Payment.objects.filter(invoice__person_id__in=wards_persons, is_active=True).select_related('invoice__person')

    return Payment.objects.none()
