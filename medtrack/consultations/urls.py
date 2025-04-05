from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('doctor-dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('calendar/', views.all_consultations, name='consultation_calendar'),
    path('calendar-physician/<int:physician_id>/', views.consultations_by_physician, name='consultation_calendar_physician'),
    path('schedule/', views.schedule_consultation, name='schedule_consultation'),
    path('cancel/<int:consultation_id>/', views.cancel_consultation, name='cancel_consultation'),
    path('reschedule/<int:consultation_id>/', views.reschedule_consultation, name='reschedule_consultation'),
      # Other URLs...
]