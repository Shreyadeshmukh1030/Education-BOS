from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.core.api_views import ModuleDefinitionViewSet, OrganizationModuleViewSet
from apps.accounts.api_views import RoleViewSet, UserViewSet
from apps.organizations.api_views import OrganizationTypeViewSet, OrganizationViewSet, CampusViewSet, DepartmentViewSet
from apps.people.api_views import PersonViewSet, StudentProfileViewSet, InstructorProfileViewSet, StaffProfileViewSet, GuardianProfileViewSet
from apps.academics.api_views import AcademicSessionViewSet, ProgramViewSet, AcademicTermViewSet, SubjectViewSet, SubjectOfferingViewSet
from apps.enrollment.api_views import EnrollmentViewSet
from apps.operations.api_views import TimetableViewSet, ClassScheduleViewSet, AttendanceRecordViewSet
from apps.assessment.api_views import AssessmentTypeViewSet, AssessmentViewSet, ResultViewSet
from apps.finance.api_views import FeeStructureViewSet, InvoiceViewSet, PaymentViewSet
from apps.communication.api_views import MessageViewSet, NotificationViewSet
from apps.configuration.api_views import GlobalSettingViewSet

router = DefaultRouter()

router.register(r'core/modules', ModuleDefinitionViewSet, basename='modules')
router.register(r'core/organization-modules', OrganizationModuleViewSet, basename='org-modules')
router.register(r'accounts/roles', RoleViewSet, basename='accounts-role')
router.register(r'accounts/users', UserViewSet, basename='accounts-user')
router.register(r'organizations/organizationtypes', OrganizationTypeViewSet, basename='organizations-organizationtype')
router.register(r'organizations/organizations', OrganizationViewSet, basename='organizations-organization')
router.register(r'organizations/campuss', CampusViewSet, basename='organizations-campus')
router.register(r'organizations/departments', DepartmentViewSet, basename='organizations-department')
router.register(r'people/persons', PersonViewSet, basename='people-person')
router.register(r'people/studentprofiles', StudentProfileViewSet, basename='people-studentprofile')
router.register(r'people/instructorprofiles', InstructorProfileViewSet, basename='people-instructorprofile')
router.register(r'people/staffprofiles', StaffProfileViewSet, basename='people-staffprofile')
router.register(r'people/guardianprofiles', GuardianProfileViewSet, basename='people-guardianprofile')
router.register(r'academics/academicsessions', AcademicSessionViewSet, basename='academics-academicsession')
router.register(r'academics/programs', ProgramViewSet, basename='academics-program')
router.register(r'academics/academicterms', AcademicTermViewSet, basename='academics-academicterm')
router.register(r'academics/subjects', SubjectViewSet, basename='academics-subject')
router.register(r'academics/subjectofferings', SubjectOfferingViewSet, basename='academics-subjectoffering')
router.register(r'enrollment/enrollments', EnrollmentViewSet, basename='enrollment-enrollment')
router.register(r'operations/timetables', TimetableViewSet, basename='operations-timetable')
router.register(r'operations/classschedules', ClassScheduleViewSet, basename='operations-classschedule')
router.register(r'operations/attendancerecords', AttendanceRecordViewSet, basename='operations-attendancerecord')
router.register(r'assessment/assessmenttypes', AssessmentTypeViewSet, basename='assessment-assessmenttype')
router.register(r'assessment/assessments', AssessmentViewSet, basename='assessment-assessment')
router.register(r'assessment/results', ResultViewSet, basename='assessment-result')
router.register(r'finance/feestructures', FeeStructureViewSet, basename='finance-feestructure')
router.register(r'finance/invoices', InvoiceViewSet, basename='finance-invoice')
router.register(r'finance/payments', PaymentViewSet, basename='finance-payment')
router.register(r'communication/messages', MessageViewSet, basename='communication-message')
router.register(r'communication/notifications', NotificationViewSet, basename='communication-notification')
router.register(r'configuration/globalsettings', GlobalSettingViewSet, basename='configuration-globalsetting')

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
