from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('calendar/', views.consultation_calendar, name='consultation_calendar'),
    # Other URLs...
]