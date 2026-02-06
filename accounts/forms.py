"""
Hospital Management - Accounts App Forms

Registration and profile forms for user authentication.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile
from hospitals.models import City, Clinic
from doctors.models import Doctor, DoctorAvailability
from datetime import time


class PatientRegistrationForm(UserCreationForm):
    """Patient signup form - extends UserCreationForm with profile fields."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Profile is auto-created by signal; update with form data
            profile = user.profile
            profile.phone = self.cleaned_data.get('phone', '')
            profile.address = self.cleaned_data.get('address', '')
            profile.save()
        return user


class DoctorRegistrationForm(UserCreationForm):
    """Doctor signup form - creates User, UserProfile (DOCTOR), and Doctor record."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=False)
    name = forms.CharField(max_length=200, required=True, help_text="Display name (e.g. Dr. John Smith)")
    specialization = forms.CharField(max_length=200, required=True)
    city = forms.ModelChoiceField(
        queryset=City.objects.all().order_by('name'), 
        required=True, 
        empty_label="Select City",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_city'})
    )
    clinic = forms.ModelChoiceField(
        queryset=Clinic.objects.none(), 
        required=True, 
        empty_label="Select Hospital/Clinic",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_clinic'})
    )
    experience = forms.IntegerField(min_value=0, required=True, help_text="Years of experience")
    consultation_fee = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=True)
    profile_image = forms.ImageField(required=False, help_text="Upload your profile picture")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['clinic'].queryset = Clinic.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.initial.get('city'):
            self.fields['clinic'].queryset = Clinic.objects.filter(city=self.initial['city']).order_by('name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = user.profile
            profile.role = 'DOCTOR'
            profile.phone = self.cleaned_data.get('phone', '')
            profile.save()
            doctor_instance = Doctor.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                specialization=self.cleaned_data['specialization'],
                city=self.cleaned_data['city'],
                clinic=self.cleaned_data['clinic'],
                experience=self.cleaned_data['experience'],
                consultation_fee=self.cleaned_data['consultation_fee'],
                profile_image=self.cleaned_data.get('profile_image')
            )
            
            # Create default availability (Mon-Fri, 9 AM - 5 PM)
            for day in range(5):
                DoctorAvailability.objects.create(
                    doctor=doctor_instance,
                    day_of_week=day,
                    start_time=time(9, 0),
                    end_time=time(17, 0)
                )
        return user


class UserLoginForm(AuthenticationForm):
    """Custom login form with Bootstrap styling support."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
