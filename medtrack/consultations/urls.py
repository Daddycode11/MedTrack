from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('doctor-dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('calendar/', views.all_consultations, name='consultation_calendar'),
    path('calendar-physician/<int:physician_id>/', views.consultations_by_physician, name='consultation_calendar_physician'),
    # Other URLs...
]