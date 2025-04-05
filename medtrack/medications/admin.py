from django.contrib import admin

from .models import (
    Pharmacist,
    MedicationType,
    MedicationGenericName,
    Medication,
    MedicationInventory,
    MedicationPrescription,
)

# Registering all models in the admin site
@admin.register(Pharmacist)
class PharmacistAdmin(admin.ModelAdmin):
    list_display = ('username', 'employee_type', 'phone_number', 'address')
    search_fields = ('username__username', 'username__first_name', 'username__last_name', 'phone_number')

@admin.register(MedicationType)
class MedicationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(MedicationGenericName)
class MedicationGenericNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'medication_type')
    search_fields = ('name', 'medication_type__name')

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic_name', 'dosage_form', 'strength', 'route_of_administration', 'manufacturer')
    search_fields = ('name', 'generic_name__name', 'manufacturer')
    list_filter = ('dosage_form', 'route_of_administration')

@admin.register(MedicationInventory)
class MedicationInventoryAdmin(admin.ModelAdmin):
    list_display = ('medication', 'quantity', 'expiration_date', 'location')
    search_fields = ('medication__name', 'location')
    list_filter = ('expiration_date',)

@admin.register(MedicationPrescription)
class MedicationPrescriptionAdmin(admin.ModelAdmin):
    list_display = ('pdl_profile', 'medication', 'dosage', 'frequency', 'duration', 'prescribed_by')
    search_fields = ('pdl_profile__username__username', 'medication__name', 'prescribed_by__username__username')
    list_filter = ('prescribed_by',)
