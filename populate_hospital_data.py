
import os
import django
import random
from datetime import datetime, time, date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management.settings')
django.setup()

from django.contrib.auth.models import User
from hospitals.models import City, Clinic
from doctors.models import Doctor, DoctorAvailability
from appointments.models import Appointment
from accounts.models import UserProfile

def create_data():
    print("Creating Cities...")
    city_names = ['Hyderabad', 'Bangalore', 'Chennai', 'Mumbai']
    city_objs = {}
    for c_name in city_names:
        city, _ = City.objects.get_or_create(name=c_name)
        city_objs[c_name] = city

    print("Creating Clinics...")
    # Dictionary of City -> [Clinic Names]
    clinic_data = {
        'Hyderabad': ['Apollo Jubilee Hills', 'Yashoda Somajiguda', 'Continental Hospital'],
        'Bangalore': ['Manipal Hospital', 'Narayana Health', 'Fortis BG Road'],
        'Chennai': ['Apollo Greams Road', 'MIOT International'],
        'Mumbai': ['Lilavati Hospital', 'Breach Candy Hospital', 'Kokilaben Hospital']
    }
    
    clinic_objs = []
    for city_name, clinics in clinic_data.items():
        city = city_objs[city_name]
        for c_name in clinics:
             # Look up by name AND city to avoid cross-city dups if names were same
             clinic, _ = Clinic.objects.get_or_create(
                name=c_name,
                defaults={
                    'city': city,
                    'address': f"Located in {city_name}"
                }
             )
             if not clinic.city_id:
                 clinic.city = city
                 clinic.save()
             clinic_objs.append(clinic)

    print("Creating Doctors...")
    # (City, Specialization, Name, Fee)
    # (City, Specialization, Name, Fee)
    doctor_specs = [
        ('Hyderabad', 'Cardiologist', 'Dr. Ramesh Gupta', 1500),
        ('Bangalore', 'Neurologist', 'Dr. Meera Nambiar', 2000),
        ('Chennai', 'Orthopedic', 'Dr. Senthil Kumar', 1400),
    ]

    doctors = []
    for city_key, spec, name, fee in doctor_specs:
        username = name.lower().replace(' ', '').replace('.', '')
        email = f"{username}@hospital.com"
        
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        if user_created:
            user.set_password('password123')
            user.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'DOCTOR'})
        else:
             UserProfile.objects.get_or_create(user=user, defaults={'role': 'DOCTOR'})

        # Find a clinic in this city
        city_obj = city_objs[city_key]
        city_clinics = Clinic.objects.filter(city=city_obj)
        if city_clinics.exists():
            assigned_clinic = city_clinics.first()
        else:
            # Fallback
            assigned_clinic = clinic_objs[0]

        doc, created = Doctor.objects.get_or_create(
            user=user,
            defaults={
                'name': name,
                'specialization': spec,
                'city': city_obj,
                'clinic': assigned_clinic,
                'experience': random.randint(5, 25),
                'consultation_fee': fee
            }
        )
        # Fix city/clinic if they don't match (for existing data updates)
        if doc.city != city_obj:
            doc.city = city_obj
            doc.clinic = assigned_clinic
            doc.save()
            
        doctors.append(doc)
        
        # Add Availability
        if not DoctorAvailability.objects.filter(doctor=doc).exists():
            for day in range(7): # Mon-Sun
                DoctorAvailability.objects.create(
                    doctor=doc,
                    day_of_week=day,
                    start_time=time(9, 0),
                    end_time=time(17, 0)
                )

    print("Creating Patients...")
    patient_names = ['rahul', 'sneha', 'vikram']
    patients = []
    for p_name in patient_names:
        user, user_created = User.objects.get_or_create(
            username=p_name,
            defaults={'email': f"{p_name}@gmail.com"}
        )
        if user_created:
            user.set_password('password123')
            user.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'PATIENT'})
        else:
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'PATIENT'})
        patients.append(user)

    print("Creating Appointments...")
    # Create some past and future appointments
    today = date.today()
    
    # 1. Past Appointment (Completed)
    Appointment.objects.get_or_create(
        doctor=doctors[0],
        patient=patients[0],
        date=today - timedelta(days=5),
        time=time(10, 0),
        defaults={
            'status': 'COMPLETED',
            'notes': "Regular checkup"
        }
    )

    # 2. Upcoming Appointment (Pending)
    Appointment.objects.get_or_create(
        doctor=doctors[1],
        patient=patients[0],
        date=today + timedelta(days=2),
        time=time(11, 30),
        defaults={
            'status': 'APPROVED',
            'notes': "Skin allergy follow up"
        }
    )

    # 3. Today's Appointment
    Appointment.objects.get_or_create(
        doctor=doctors[0],
        patient=patients[1],
        date=today,
        time=time(14, 0),
        defaults={
            'status': 'PENDING',
            'notes': "Heartbeat irregularity"
        }
    )

    print("Done! Data populated.")
    print("Doctor Login: drrameshgupta / password123 (Hyderabad)")
    print("Patient Login: rahul / password123")

if __name__ == '__main__':
    create_data()
