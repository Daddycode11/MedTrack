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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pdl/', include('pdl.urls')),  # Include the URLs from the pdl app
    path('consultations/', include('consultations.urls')),  # Include the URLs from the consultations app
    path('medications/', include('medications.urls')),  # Include the URLs from the medications app
]

# redirect root URL to pdl app
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/pdl/', permanent=True)),
]