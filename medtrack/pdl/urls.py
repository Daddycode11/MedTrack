from django.urls import path
from . import views

app_name = 'pdl'

urlpatterns = [
    path('', views.index, name='index'),
    path('pdl/list', views.pdl_list, name='pdl_list'),
]