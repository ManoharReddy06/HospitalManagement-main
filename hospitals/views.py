"""
Hospital Management - Hospitals App Views

Clinic and Lab listing views.
"""
from django.shortcuts import render
from .models import Clinic, Lab


def clinic_list(request):
    """List all clinics with optional city filter."""
    clinics = Clinic.objects.select_related('city').order_by('city__name', 'name')
    city_filter = request.GET.get('city')
    if city_filter:
        clinics = clinics.filter(city__name__icontains=city_filter)
    return render(request, 'hospitals/clinic_list.html', {'clinics': clinics})


def lab_list(request):
    """List all labs with optional city filter."""
    labs = Lab.objects.select_related('city').order_by('city__name', 'name')
    city_filter = request.GET.get('city')
    if city_filter:
        labs = labs.filter(city__name__icontains=city_filter)
    
    # Mock data if empty
    if not labs.exists() and not city_filter:
        labs = [
            {'name': 'City Diagnotics', 'city': {'name': 'Hyderabad'}, 'address': 'Jubilee Hills, Rd 36', 'test_types': 'Blood Test, MRI, X-Ray', 'timings': '24/7'},
            {'name': 'Apollo Diagnostics', 'city': {'name': 'Bangalore'}, 'address': 'Indiranagar', 'test_types': 'Full Body Checkup, CT Scan', 'timings': '7:00 AM - 9:00 PM'},
            {'name': 'Metro Labs', 'city': {'name': 'Chennai'}, 'address': 'Anna Nagar', 'test_types': 'Thyroid, Diabetes, Lipid Profile', 'timings': '8:00 AM - 8:00 PM'},
        ]
        
    return render(request, 'hospitals/lab_list.html', {'labs': labs})


from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET

@require_GET
def get_clinics_by_city(request):
    city_id = request.GET.get('city_id')
    if not city_id:
        return JsonResponse({'clinics': []})
    
    clinics = Clinic.objects.filter(city_id=city_id).values('id', 'name').order_by('name')
    return JsonResponse({'clinics': list(clinics)})
