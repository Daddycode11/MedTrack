from django.contrib import admin
from .models import DetentionStatus, PDLProfile, DetentionReason, DetentionInstance


# Register your models here.

@admin.register(DetentionStatus)
class DetentionStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'description')
    search_fields = ('status',)
    list_filter = ('status',)
    ordering = ('status',)
    fieldsets = (
        (None, {
            'fields': ('status', 'description')
        }),
    )
    list_per_page = 10
    list_display_links = ('status',)

@admin.register(PDLProfile)
class PDLProfileAdmin(admin.ModelAdmin):
    list_display = ('username__first_name', 'username__last_name', 'phone_number')
    search_fields = ('username__first_name', 'username__last_name')
    list_filter = ('username__first_name',)
    ordering = ('username__last_name',)
    fieldsets = (
        (None, {
            'fields': ('username', 'phone_number')
        }),
    )
    list_per_page = 10
    list_display_links = ('username__first_name',)

@admin.register(DetentionReason)
class DetentionReasonAdmin(admin.ModelAdmin):
    list_display = ('reason', 'description')
    search_fields = ('reason',)
    list_filter = ('reason',)
    ordering = ('reason',)
    fieldsets = (
        (None, {
            'fields': ('reason', 'description')
        }),
    )
    list_per_page = 10
    list_display_links = ('reason',)

@admin.register(DetentionInstance)
class DetentionInstanceAdmin(admin.ModelAdmin):
    list_display = ('pdl_profile', 'detention_status', 'detention_start_date', 'detention_end_date', 'detention_reason')
    search_fields = ('pdl_profile__username__first_name', 'pdl_profile__username__last_name', 'detention_status__status', 'detention_reason__reason')
    list_filter = ('detention_status', 'detention_reason')
    ordering = ('-detention_start_date',)
    fieldsets = (
        (None, {
            'fields': ('pdl_profile', 'detention_status', 'detention_start_date', 'detention_end_date', 'detention_reason', 'notes')
        }),
    )
    list_per_page = 10
    list_display_links = ('pdl_profile',)