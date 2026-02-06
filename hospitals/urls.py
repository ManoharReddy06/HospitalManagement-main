"""
Hospital Management - Hospitals App URLs
"""
from django.urls import path
from . import views

app_name = 'hospitals'

urlpatterns = [
    path('clinics/', views.clinic_list, name='clinic_list'),
    path('labs/', views.lab_list, name='lab_list'),
    path('ajax/clinics/', views.get_clinics_by_city, name='get_clinics_by_city'),
]
