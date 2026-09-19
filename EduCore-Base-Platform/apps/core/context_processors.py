from .permissions import (
    get_user_role,
    ROLE_SUPER_ADMIN,
    ROLE_ORG_ADMIN,
    ROLE_INSTRUCTOR,
    ROLE_STUDENT,
    ROLE_PARENT,
    ROLE_ACCOUNTANT,
    ROLE_STAFF,
)

def rbac_context(request):
    """
    Exposes canonical role and permission flags to all templates.
    """
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {
            'user_role': None,
            'is_admin': False,
            'is_super_admin': False,
            'is_org_admin': False,
            'is_instructor': False,
            'is_student': False,
            'is_parent': False,
            'is_accountant': False,
            'is_staff_role': False,
        }

    role = get_user_role(request.user)
    is_super = (role == ROLE_SUPER_ADMIN)
    is_org = (role == ROLE_ORG_ADMIN)
    is_admin = is_super or is_org
    is_inst = (role == ROLE_INSTRUCTOR)
    is_stu = (role == ROLE_STUDENT)
    is_parent = (role == ROLE_PARENT)
    is_acc = (role == ROLE_ACCOUNTANT)
    is_staff = (role == ROLE_STAFF)

    return {
        'user_role': role,
        'is_admin': is_admin,
        'is_super_admin': is_super,
        'is_org_admin': is_org,
        'is_instructor': is_inst,
        'is_student': is_stu,
        'is_parent': is_parent,
        'is_accountant': is_acc,
        'is_staff_role': is_staff,
        # Action capability flags
        'can_view_finance': is_admin or is_acc or is_stu or is_parent,
        'can_manage_finance': is_admin or is_acc,
        'can_view_reports': is_admin or is_acc or is_inst,
        'can_manage_academics': is_admin,
        'can_manage_operations': is_admin or is_inst,
        'can_manage_settings': is_admin,
    }
