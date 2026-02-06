from django.contrib import admin
from .models import Doctor, DoctorAvailability


class DoctorAvailabilityInline(admin.TabularInline):
    model = DoctorAvailability
    extra = 1


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'city', 'clinic', 'consultation_fee', 'experience']
    list_filter = ['city', 'specialization']
    search_fields = ['name', 'specialization']
    inlines = [DoctorAvailabilityInline]


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time']
    list_filter = ['day_of_week']
