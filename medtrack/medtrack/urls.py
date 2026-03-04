"""
URL configuration for medtrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pdl/', include('pdl.urls')),
    path('consultations/', include('consultations.urls')),
    path('medications/', include('medications.urls')),
    path('reports/', include('reports.urls')),
    path('user-guide/', TemplateView.as_view(template_name='user_guide.html'), name='user_guide'),
    # Add other URL patterns as needed
]

# redirect root URL to pdl app
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/pdl/', permanent=True)),
]