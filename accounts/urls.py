"""
Hospital Management - Accounts App URLs
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.PatientRegisterView.as_view(), name='register'),
    path('register/doctor/', views.DoctorRegisterView.as_view(), name='register_doctor'),
    path('location/', views.location_page, name='location'),

]
