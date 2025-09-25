from django.urls import path
from . import views

app_name = 'medications'

urlpatterns = [
    path('list/', views.medication_list, name='medication_list'),
    path('prescriptions/<int:medication_id>/', views.prescription_list, name='prescription_list'),
     path("prescriptions/new/", views.prescription_create, name="prescription_create"),
    # Stub detail view route; implement later if you don’t have it yet:
    path("prescriptions/details/r<int:pk>/", views.prescription_detail, name="prescription_detail"),

]