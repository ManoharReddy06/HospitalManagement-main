# Hospital Management System

A complete Hospital Management System built with Django, featuring patient registration, appointment booking, doctor management, and role-based dashboards.

## Features

- **User Authentication**: Registration, Login, Logout
- **Role-Based Access**: Patient, Doctor, Admin
- **Patient Dashboard**: Book appointments, view history, browse doctors & clinics
- **Doctor Dashboard**: View assigned appointments, manage availability
- **Appointment System**: Book with city → clinic → doctor flow, prevent double booking
- **Doctor Profiles**: Specialization, fees, availability, profile image
- **Clinics & Labs**: Browse by city with filtering

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Load Sample Data

```bash
python manage.py load_sample_data
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Sample Login Credentials

| Role   | Username  | Password   |
|--------|-----------|------------|
| Patient| patient1  | patient123 |
| Doctor | doctor1   | doctor123  |
| Admin  | admin     | admin123   |

## Project Structure

```
project/
├── accounts/          # User auth, registration, profiles
├── appointments/      # Appointment booking, patient dashboard
├── doctors/           # Doctor listing, profiles, doctor dashboard
├── hospitals/         # Cities, clinics, labs
├── hospital_management/  # Project settings
├── templates/         # HTML templates
├── static/            # Static files
└── manage.py
```

## URL Structure

- `/` - Dashboard (redirects by role)
- `/login/` - Login
- `/register/` - Patient registration
- `/doctors/` - Doctor list
- `/doctors/<id>/` - Doctor detail
- `/doctors/dashboard/` - Doctor dashboard
- `/appointments/` - Patient dashboard
- `/appointments/book/` - Book appointment
- `/appointments/history/` - Appointment history
- `/hospitals/clinics/` - Clinic list
- `/hospitals/labs/` - Lab list
- `/admin/` - Django admin

## Models Overview

- **UserProfile**: Extends User with role (Patient/Doctor/Admin)
- **City, Clinic, Lab**: Healthcare facilities
- **Doctor**: Linked to User, Clinic; has specialization, fee, availability
- **DoctorAvailability**: Day of week + time range per doctor
- **Appointment**: Patient, doctor, date, time_slot, service, status

## Admin Panel

Access `/admin/` with admin credentials to:
- Manage users, doctors, clinics, labs
- Update appointment status (Pending/Approved/Completed)
- Add doctor availability
- Create new doctors (link to User for doctor login)
