"""
Hospital Management - Hospitals App Models

City: Locations where clinics and labs operate
Clinic: Healthcare facilities (hospitals/clinics)
Lab: Laboratory facilities for tests
"""
from django.db import models


class City(models.Model):
    """Cities where healthcare facilities are located."""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Clinic(models.Model):
    """Hospitals/Clinics - healthcare facilities."""
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='clinics')
    address = models.TextField()

    class Meta:
        verbose_name_plural = "Clinics"

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class Lab(models.Model):
    """Laboratory facilities for diagnostic tests."""
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='labs')
    address = models.TextField()
    test_types = models.TextField(
        help_text="Comma-separated list of test types (e.g., Blood Test, X-Ray, MRI)"
    )
    timings = models.CharField(
        max_length=200,
        help_text="e.g., 8:00 AM - 8:00 PM"
    )

    class Meta:
        verbose_name_plural = "Labs"

    def __str__(self):
        return f"{self.name} - {self.city.name}"
