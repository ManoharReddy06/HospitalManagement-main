"""
Management command to load sample data for Hospital Management System.
Usage: python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import time
from accounts.models import UserProfile
from hospitals.models import City, Clinic, Lab
from doctors.models import Doctor, DoctorAvailability


class Command(BaseCommand):
    help = 'Load sample data: cities, clinics, labs, doctors, and test users'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')

        # Cities
        cities_data = [
            ('Mumbai',),
            ('Delhi',),
            ('Bangalore',),
        ]
        cities = {}
        for name, in cities_data:
            city, _ = City.objects.get_or_create(name=name)
            cities[name] = city
        self.stdout.write(f'  Created {len(cities)} cities')

        # Clinics
        clinics_data = [
            ('City Hospital', 'Mumbai', '123 Main Street, Andheri West'),
            ('Metro Clinic', 'Mumbai', '456 Linking Road, Bandra'),
            ('Apollo Hospital', 'Delhi', 'Sector 18, Noida'),
            ('Medanta', 'Delhi', 'Saket, South Delhi'),
            ('Fortis Hospital', 'Bangalore', 'Cunningham Road'),
        ]
        clinics = {}
        for name, city_name, address in clinics_data:
            clinic, _ = Clinic.objects.get_or_create(
                name=name,
                defaults={'city': cities[city_name], 'address': address}
            )
            clinics[name] = clinic
        self.stdout.write(f'  Created {len(clinics)} clinics')

        # Labs
        labs_data = [
            ('PathLab Diagnostics', 'Mumbai', 'Blood Test, Urine Test, CBC', '8:00 AM - 8:00 PM'),
            ('Dr. Lal PathLabs', 'Mumbai', 'Blood Test, X-Ray, MRI, ECG', '7:00 AM - 9:00 PM'),
            ('Thyrocare', 'Delhi', 'Blood Test, Thyroid, Diabetes', '6:00 AM - 10:00 PM'),
            ('Metropolis Lab', 'Bangalore', 'Blood Test, Covid RT-PCR', '24 Hours'),
        ]
        for name, city_name, test_types, timings in labs_data:
            Lab.objects.get_or_create(
                name=name,
                city=cities[city_name],
                defaults={'address': f'{name}, {cities[city_name].name}', 'test_types': test_types, 'timings': timings}
            )
        self.stdout.write(f'  Created labs')

        # Doctors
        doctors_data = [
            ('Rajesh Kumar', 'Cardiologist', 'Mumbai', 'City Hospital', 15, 1500),
            ('Priya Sharma', 'Pediatrician', 'Mumbai', 'Metro Clinic', 10, 800),
            ('Amit Singh', 'General Physician', 'Delhi', 'Apollo Hospital', 20, 1200),
            ('Sneha Reddy', 'Dermatologist', 'Bangalore', 'Fortis Hospital', 8, 1000),
        ]
        for name, spec, city_name, clinic_name, exp, fee in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                name=name,
                specialization=spec,
                defaults={
                    'city': cities[city_name],
                    'clinic': clinics[clinic_name],
                    'experience': exp,
                    'consultation_fee': fee,
                }
            )
            if created:
                # Add availability (Mon-Fri, 9 AM - 5 PM)
                for day in range(5):  # Mon to Fri
                    DoctorAvailability.objects.get_or_create(
                        doctor=doctor,
                        day_of_week=day,
                        defaults={'start_time': time(9, 0), 'end_time': time(17, 0)}
                    )
        self.stdout.write(f'  Created doctors with availability')

        # Test Patient
        if not User.objects.filter(username='patient1').exists():
            user = User.objects.create_user(
                username='patient1',
                password='patient123',
                email='patient@test.com',
                first_name='Test',
                last_name='Patient'
            )
            profile = user.profile
            profile.role = 'PATIENT'
            profile.phone = '9876543210'
            profile.save()
            self.stdout.write('  Created test patient: patient1 / patient123')

        # Test Doctor User
        if not User.objects.filter(username='doctor1').exists():
            user = User.objects.create_user(
                username='doctor1',
                password='doctor123',
                email='doctor@test.com',
                first_name='Rajesh',
                last_name='Kumar'
            )
            profile = user.profile
            profile.role = 'DOCTOR'
            profile.save()
            doctor = Doctor.objects.get(name='Rajesh Kumar')
            doctor.user = user
            doctor.save()
            self.stdout.write('  Created test doctor: doctor1 / doctor123')

        # Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@hospital.com', 'admin123')
            admin_user = User.objects.get(username='admin')
            profile = admin_user.profile
            profile.role = 'ADMIN'
            profile.save()
            self.stdout.write('  Created admin: admin / admin123')

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
