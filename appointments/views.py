from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Appointment
from doctors.models import Doctor, DoctorAvailability
from accounts.decorators import patient_required


@patient_required
def patient_dashboard(request):
    appointments = request.user.patient_appointments.all()
    latest_doctors = Doctor.objects.select_related('user').order_by('-id')[:3]

    return render(request, 'appointments/patient_dashboard.html', {
        'appointments': appointments,
        'doctors': latest_doctors
    })


@patient_required
def appointment_history(request):
    appointments = request.user.patient_appointments.all()

    return render(request, 'appointments/appointment_history.html', {
        'appointments': appointments
    })


@patient_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        date_val = request.POST.get('date')
        time_val = request.POST.get('time')
        notes = request.POST.get('notes')

        Appointment.objects.create(
            doctor=doctor,
            patient=request.user,
            date=date_val,
            time=time_val,
            status='PENDING',
            notes=notes
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect('appointments:patient_dashboard')

    return render(request, 'appointments/book_appointment.html', {
        'doctor': doctor,
        'today': date.today()
    })


@patient_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        patient=request.user
    )

    appointment.status = 'CANCELLED'
    appointment.save()

    messages.success(request, "Appointment cancelled successfully. You may book another appointment.")
    return redirect('doctors:doctor_list')


def get_available_slots(request):
    doctor_id = request.GET.get('doctor_id')
    date_str = request.GET.get('date')

    if not doctor_id or not date_str:
        return JsonResponse({'slots': []})

    try:
        print(f"DEBUG: Fetching slots for Doctor ID: {doctor_id}, Date: {date_str}")
        doctor = Doctor.objects.get(id=doctor_id)
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = selected_date.weekday()
        print(f"DEBUG: Day of week: {day_of_week}")

        availability = DoctorAvailability.objects.filter(
            doctor=doctor,
            day_of_week=day_of_week
        ).first()

        if not availability:
            print(f"DEBUG: No availability found for Doctor {doctor.name} on day {day_of_week}")
            return JsonResponse({'slots': []})
        
        print(f"DEBUG: Found availability: {availability.start_time} - {availability.end_time}")

        # Generate slots
        slots = []
        current_time = datetime.combine(selected_date, availability.start_time)
        end_time = datetime.combine(selected_date, availability.end_time)

        # Get existing appointments
        existing_appointments = Appointment.objects.filter(
            doctor=doctor,
            date=selected_date,
            status__in=['PENDING', 'APPROVED']
        ).values_list('time', flat=True)
        
        print(f"DEBUG: Existing appointments at: {list(existing_appointments)}")

        while current_time < end_time:
            time_val = current_time.time()
            
            # Check if slot is booked
            is_booked = time_val in existing_appointments
            
            slots.append({
                'value': time_val.strftime('%H:%M'),
                'label': current_time.strftime('%I:%M %p'),
                'is_booked': is_booked
            })

            current_time += timedelta(minutes=30)  # 30 min intervals

        # Filter out Lunch Break (12:00 PM - 1:00 PM)
        # We need to filter the *generated* slots list or avoid adding them.
        # Let's rewrite the loop slightly or filter 'slots' list
        final_slots = []
        for slot in slots:
            # slot['value'] is "HH:MM" e.g. "12:00", "12:30"
            t_str = slot['value']
            h = int(t_str.split(':')[0])
            # Remove 12:00 and 12:30
            if h == 12:
                continue
            final_slots.append(slot)
            
        print(f"DEBUG: Returning {len(final_slots)} slots")
        return JsonResponse({'slots': final_slots})

    except Exception as e:
        import traceback
        print(f"DEBUG: Error: {e}")
        traceback.print_exc()
        return JsonResponse({'slots': [], 'error': str(e)})


from accounts.decorators import doctor_required

@doctor_required
def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user.doctor_profile)
    
    if status in ['APPROVED', 'CANCELLED']:
        appointment.status = status
        appointment.save()
        messages.success(request, f"Appointment marked as {status}.")
    
    return redirect('doctors:dashboard')
