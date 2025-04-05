from django.urls import path
from . import views

app_name = 'medications'

urlpatterns = [
    path('list/', views.medication_list, name='medication_list'),
    path('prescriptions/<int:medication_id>/', views.prescription_list, name='prescription_list'),
]