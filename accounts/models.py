"""
Hospital Management - Accounts App Models

UserProfile: Extends Django User with role-based access (Patient, Doctor, Admin)
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with role for access control."""
    ROLE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PATIENT')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    @property
    def is_patient(self):
        return self.role == 'PATIENT'

    @property
    def is_doctor(self):
        return self.role == 'DOCTOR'

    @property
    def is_admin(self):
        return self.role == 'ADMIN'
