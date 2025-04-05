from django.contrib import admin

# Register your models here.
from .models import MedicalSpecialty, Physician, ConsultationLocation, ConsultationReason, Consultation

@admin.register(MedicalSpecialty)
class MedicalSpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
    )

@admin.register(Physician)
class PhysicianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'employee_type', 'specialty', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name',)
    list_filter = ('employee_type', 'specialty')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'employee_type', 'specialty')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Address Information', {
            'fields': ('address',)
        }),
    )

@admin.register(ConsultationLocation)
class ConsultationLocationAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'capacity')
    search_fields = ('room_number',)
    ordering = ('room_number',)
    list_filter = ('capacity',)
    fieldsets = (
        (None, {
            'fields': ('room_number', 'capacity')
        }),
    )

@admin.register(ConsultationReason)
class ConsultationReasonAdmin(admin.ModelAdmin):
    list_display = ('reason',)
    search_fields = ('reason',)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        'pdl_profile',
        'physician',
        'location',
        'reason',
        'status',
        'consultation_date_date_only',
        'consultation_time_block',
        'is_an_emergency',
    )
    search_fields = (
        'pdl_profile__first_name',
        'pdl_profile__last_name',
        'physician__first_name',
        'physician__last_name',
    )
    list_filter = ('status', 'is_an_emergency', 'consultation_date_date_only', 'consultation_time_block')