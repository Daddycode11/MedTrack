from django.urls import path
from . import views

app_name = 'pdl'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.pdl_list, name='pdl_list'),  # Example existing URL
    path('profile/<str:username>/', views.pdl_profile, name='pdl_profile_by_id'),  # New URL
    path('add/', views.add_pdl, name='add_pdl'),  # New URL for adding PDL
    path("api/pdl/<int:pk>/latest-room/", views.pdl_detention_room_api, name="pdl_latest_room_api"),
    path("edit/<int:pdl_id>/", views.edit_pdl, name="edit_pdl"),
    path("p/<int:pk>/delete/", views.delete_pdl, name="delete_pdl"),
]