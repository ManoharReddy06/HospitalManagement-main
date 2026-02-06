from django.urls import path
from . import views

app_name = "doctors"

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('search/', views.search_doctors, name='search_doctors'),
    path('<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('get-doctors-by-city/', views.get_doctors_by_city, name='get_doctors_by_city'),
]
