from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization, Campus, Department
from .forms import OrganizationForm
from apps.academics.models import Program
from apps.core.permissions import role_required, ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN
from apps.core.audit import log_audit

@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN)
def organization_list(request):
    organizations = Organization.objects.filter(is_active=True).prefetch_related('campuses', 'departments')
    campuses = Campus.objects.filter(is_active=True).select_related('organization')
    departments = Department.objects.filter(is_active=True).select_related('organization')
    
    total_programs = Program.objects.filter(is_active=True).count()
    
    context = {
        'organizations': organizations,
        'campuses': campuses,
        'departments': departments,
        'total_programs': total_programs,
        'total_campuses': campuses.count(),
        'total_departments': departments.count(),
    }
    return render(request, 'organizations/organization_list.html', context)

@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN)
def organization_create(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            org = form.save()
            log_audit(
                action="CREATE",
                resource="Organization",
                resource_id=org.id,
                description=f"Created institutional organization '{org.name}'",
                request=request
            )
            return redirect('organizations:detail', pk=org.pk)
    else:
        form = OrganizationForm()
    return render(request, 'organizations/organization_form.html', {'form': form, 'title': 'Add Institutional Campus / Entity'})

@login_required
@role_required(ROLE_SUPER_ADMIN, ROLE_ORG_ADMIN)
def organization_detail(request, pk):
    organization = get_object_or_404(Organization, pk=pk, is_active=True)
    campuses = organization.campuses.filter(is_active=True)
    departments = organization.departments.filter(is_active=True)
    
    context = {
        'organization': organization,
        'campuses': campuses,
        'departments': departments,
    }
    return render(request, 'organizations/organization_detail.html', context)
