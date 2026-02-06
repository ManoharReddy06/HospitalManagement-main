from django.contrib import admin
from .models import City, Clinic, Lab


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address']
    list_filter = ['city']
    search_fields = ['name', 'city__name']


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'timings']
    list_filter = ['city']
    search_fields = ['name', 'city__name']
