from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('config.api_urls')),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('organizations/', include('apps.organizations.urls')),
    path('people/', include('apps.people.urls')),
    path('academics/', include('apps.academics.urls')),
    path('enrollment/', include('apps.enrollment.urls')),
    path('operations/', include('apps.operations.urls')),
    path('assessment/', include('apps.assessment.urls')),
    path('finance/', include('apps.finance.urls')),
    path('communication/', include('apps.communication.urls')),
    path('configuration/', include('apps.configuration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
