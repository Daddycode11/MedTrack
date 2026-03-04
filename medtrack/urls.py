
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('pdl:login'), name='home'),
    path('admin/', admin.site.urls),
    path('pdl/', include('pdl.urls')),
    path('consultations/', include('consultations.urls')),
    path('medications/', include('medications.urls')),
    path('reports/', include('reports.urls')),
    path('user-guide/', TemplateView.as_view(template_name='user_guide.html'), name='user_guide'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
