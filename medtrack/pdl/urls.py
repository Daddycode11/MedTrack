from django.urls import path
from . import views

app_name = 'pdl'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.pdl_list, name='pdl_list'),  # Example existing URL
    path('profile/<int:pk>/', views.pdl_profile, name='pdl_profile'),  # New URL
    path('add/', views.add_pdl, name='add_pdl'),  # New URL for adding PDL
]