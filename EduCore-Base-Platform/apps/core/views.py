from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .module_registry import get_enabled_modules

@login_required
def dashboard(request):
    enabled_modules = get_enabled_modules()
    context = {
        'enabled_modules': enabled_modules,
    }
    return render(request, 'pages/dashboard.html', context)
