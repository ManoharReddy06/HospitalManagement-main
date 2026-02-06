"""
Hospital Management - Doctors App Models

Doctor: Doctor profile with details, linked to User for login
DoctorAvailability: Available days and time slots per doctor
"""
from django.db import models
from django.contrib.auth.models import User
from hospitals.models import City, Clinic


class Doctor(models.Model):
    """Doctor profile with full details."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='doctor_profile',
        null=True, blank=True  # Admin-created doctors may not have user account
    )
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='doctors')
    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name='doctors',
        help_text="Primary hospital/clinic"
    )
    experience = models.IntegerField(help_text="Years of experience")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    profile_image = models.ImageField(
        upload_to='doctors/', blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "Doctors"

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"


class DoctorAvailability(models.Model):
    """Doctor's available days and time slots."""
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='availabilities'
    )
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name_plural = "Doctor Availabilities"
        unique_together = ['doctor', 'day_of_week']

    def __str__(self):
        return f"{self.doctor.name} - {self.get_day_of_week_display()}"
