from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GlobalSetting
from .forms import GlobalSettingForm

@login_required
def setting_list(request):
    settings = GlobalSetting.objects.filter(is_active=True).order_by('key')
    return render(request, 'configuration/setting_list.html', {'settings': settings})

@login_required
def setting_create(request):
    if request.method == 'POST':
        form = GlobalSettingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('configuration:index')
    else:
        form = GlobalSettingForm()
    return render(request, 'configuration/setting_form.html', {'form': form, 'title': 'Create Setting'})

@login_required
def setting_edit(request, pk):
    setting = get_object_or_404(GlobalSetting, pk=pk)
    if request.method == 'POST':
        form = GlobalSettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('configuration:index')
    else:
        form = GlobalSettingForm(instance=setting)
    return render(request, 'configuration/setting_form.html', {'form': form, 'title': f'Edit {setting.key}'})
