# reports/urls.py
from django.urls import path
from .views import report_center, report_details

app_name = 'reports'
urlpatterns = [
    path("", report_center, name="report_center"),
    path("report-center/details/", report_details, name="report_details"),
]
