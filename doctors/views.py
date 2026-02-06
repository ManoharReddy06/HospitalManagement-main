from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages
from .models import Doctor
from appointments.models import Appointment


from django.db.models import Q

def doctor_list(request):
    doctors = Doctor.objects.select_related('user').order_by('-id')
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})


def search_doctors(request):
    # Base Queryset
    doctors = Doctor.objects.select_related('user', 'city', 'clinic').order_by('-id')

    # Filter Options (Populate dropdowns)
    cities = Doctor.objects.values_list('city__name', flat=True).distinct().order_by('city__name')
    specializations = Doctor.objects.values_list('specialization', flat=True).distinct().order_by('specialization')
    clinics = Doctor.objects.values_list('clinic__name', flat=True).distinct().order_by('clinic__name')

    # Get Filter Parameters
    city_filter = request.GET.get('city')
    spec_filter = request.GET.get('specialization')
    clinic_filter = request.GET.get('clinic')

    # Apply Filters
    if city_filter:
        doctors = doctors.filter(city__name=city_filter)
    if spec_filter:
        doctors = doctors.filter(specialization=spec_filter)
    if clinic_filter:
        doctors = doctors.filter(clinic__name=clinic_filter)

    context = {
        'doctors': doctors,
        'cities': cities,
        'specializations': specializations,
        'clinics': clinics,
        'selected_city': city_filter,
        'selected_spec': spec_filter,
        'selected_clinic': clinic_filter,
    }
    return render(request, 'doctors/doctor_search.html', context)


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})


@login_required
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by('date', 'time')

    today_count = appointments.filter(date=now().date()).count()
    appointments_count = appointments.count()

    return render(
        request,
        'doctors/dashboard.html',
        {
            'doctor': doctor,
            'appointments': appointments,
            'today_count': today_count,
            'appointments_count': appointments_count,
        }
    )


def get_doctors_by_city(request):
    city = request.GET.get('city')

    doctors = Doctor.objects.filter(city__iexact=city)

    data = [
        {
            'id': doctor.id,
            'name': doctor.user.get_full_name() or doctor.user.username,
            'specialization': doctor.specialization,
        }
        for doctor in doctors
    ]

from .forms import DoctorProfileUpdateForm
from django.contrib import messages

@login_required
def update_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == 'POST':
        form = DoctorProfileUpdateForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('doctors:dashboard')
    else:
        form = DoctorProfileUpdateForm(instance=doctor)

    return render(request, 'doctors/profile_update.html', {'form': form})
