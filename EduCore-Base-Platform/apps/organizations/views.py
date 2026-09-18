from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization
from .forms import OrganizationForm

@login_required
def organization_list(request):
    organizations = Organization.objects.filter(is_active=True)
    return render(request, 'organizations/organization_list.html', {'organizations': organizations})

@login_required
def organization_create(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            org = form.save()
            return redirect('organizations:detail', pk=org.pk)
    else:
        form = OrganizationForm()
    return render(request, 'organizations/organization_form.html', {'form': form, 'title': 'Create Organization'})

@login_required
def organization_detail(request, pk):
    organization = get_object_or_404(Organization, pk=pk, is_active=True)
    return render(request, 'organizations/organization_detail.html', {'organization': organization})
