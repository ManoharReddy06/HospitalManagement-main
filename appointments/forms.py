"""
Hospital Management - Appointments App Forms

Appointment booking form with dynamic city/clinic/doctor selection.
"""
from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Appointment, TIME_SLOT_CHOICES
from hospitals.models import City, Clinic, Lab
from doctors.models import Doctor


class AppointmentBookingForm(forms.ModelForm):
    """Form for booking appointments with cascading filters."""
    city = forms.ModelChoiceField(
        queryset=City.objects.all().order_by('name'),
        required=True,
        empty_label="Select City"
    )
    clinic = forms.ModelChoiceField(
        queryset=Clinic.objects.none(),
        required=True,
        empty_label="Select Hospital/Clinic"
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.none(),
        required=True,
        empty_label="Select Doctor"
    )
    lab = forms.ModelChoiceField(
        queryset=Lab.objects.none(),
        required=False,
        empty_label="Select Lab (for Lab service)"
    )

    class Meta:
        model = Appointment
        fields = ['city', 'clinic', 'doctor', 'lab', 'date', 'time_slot', 'service', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': str(date.today())}),
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['clinic'].queryset = Clinic.objects.filter(city_id=city_id)
                self.fields['doctor'].queryset = Doctor.objects.filter(city_id=city_id)
                self.fields['lab'].queryset = Lab.objects.filter(city_id=city_id)
            except (ValueError, TypeError):
                pass
        elif self.instance and self.instance.pk:
            self.fields['clinic'].queryset = self.instance.clinic.city.clinics.all()
            self.fields['doctor'].queryset = Doctor.objects.filter(city=self.instance.doctor.city)
            self.fields['lab'].queryset = Lab.objects.filter(city=self.instance.clinic.city)

    def clean_date(self):
        d = self.cleaned_data.get('date')
        if d and d < date.today():
            raise ValidationError("Appointment date cannot be in the past.")
        return d

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date_val = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')
        service = cleaned_data.get('service')
        lab = cleaned_data.get('lab')

        if service == 'LAB' and not lab:
            raise ValidationError({'lab': 'Lab is required for Lab service.'})

        # Check double booking
        if doctor and date_val and time_slot:
            conflicting = Appointment.objects.filter(
                doctor=doctor, date=date_val, time_slot=time_slot
            ).exclude(status='CANCELLED')
            if self.instance and self.instance.pk:
                conflicting = conflicting.exclude(pk=self.instance.pk)
            if conflicting.exists():
                raise ValidationError(
                    'This time slot is already booked. Please select another slot.'
                )
        return cleaned_data
