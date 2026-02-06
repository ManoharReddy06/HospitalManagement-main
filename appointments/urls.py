from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('history/', views.appointment_history, name='appointment_history'),

    # Appointment creation (ALL routes point to same logic)
    path('slot-book/<int:doctor_id>/', views.book_appointment, name='slot_booking_entry'),
    path('create/<int:doctor_id>/', views.book_appointment, name='create'),

    path('cancel/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
    path('status/<int:pk>/<str:status>/', views.update_appointment_status, name='update_appointment_status'),         
    path('ajax/slots/', views.get_available_slots, name='get_available_slots'),
]
