from django.db import models
# User model
from django.contrib.auth.models import User

# Create your models here.
class MedicalSpecialty(models.Model):
    """
    Model representing a medical specialty.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Medical Specialty"
        verbose_name_plural = "Medical Specialties"
        ordering = ['name']

class Physician(models.Model):
    """
    Model representing a doctor.
    """
    EMPLOYEE_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
    ]

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE_CHOICES, default='full_time')
    specialty = models.ForeignKey(MedicalSpecialty, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username.first_name} {self.username.last_name} ({self.specialty})"
    class Meta:
        verbose_name = "Physician"
        verbose_name_plural = "Physicians"
        ordering = ['username__last_name']


class ConsultationLocation(models.Model):
    """
    Model representing a consultation location.
    """
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return self.room_number
    class Meta:
        verbose_name = "Consultation Location"
        verbose_name_plural = "Consultation Locations"
        ordering = ['room_number']

class ConsultationReason(models.Model):
    """
    Model representing a reason for consultation.
    """
    reason = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.reason
    class Meta:
        verbose_name = "Consultation Reason"
        verbose_name_plural = "Consultation Reasons"
        ordering = ['reason']

from pdl.models import PDLProfile
import enum

class ConsultationTimeBlock(enum.Enum):
    """
    Enum representing time 30-minute blocks for consultations, listed by start time.
    """

    BLOCK_01 = ("00:00", "00:00")
    BLOCK_02 = ("00:30", "00:30")
    BLOCK_03 = ("01:00", "01:00")
    BLOCK_04 = ("01:30", "01:30")
    BLOCK_05 = ("02:00", "02:00")
    BLOCK_06 = ("02:30", "02:30")
    BLOCK_07 = ("03:00", "03:00")
    BLOCK_08 = ("03:30", "03:30")
    BLOCK_09 = ("04:00", "04:00")
    BLOCK_10 = ("04:30", "04:30")
    BLOCK_11 = ("05:00", "05:00")
    BLOCK_12 = ("05:30", "05:30")
    BLOCK_13 = ("06:00", "06:00")
    BLOCK_14 = ("06:30", "06:30")
    BLOCK_15 = ("07:00", "07:00")
    BLOCK_16 = ("07:30", "07:30")
    BLOCK_17 = ("08:00", "08:00")
    BLOCK_18 = ("08:30", "08:30")
    BLOCK_19 = ("09:00", "09:00")
    BLOCK_20 = ("09:30", "09:30")
    BLOCK_21 = ("10:00", "10:00")
    BLOCK_22 = ("10:30", "10:30")
    BLOCK_23 = ("11:00", "11:00")
    BLOCK_24 = ("11:30", "11:30")
    BLOCK_25 = ("12:00", "12:00")
    BLOCK_26 = ("12:30", "12:30")
    BLOCK_27 = ("13:00", "13:00")
    BLOCK_28 = ("13:30", "13:30")
    BLOCK_29 = ("14:00", "14:00")
    BLOCK_30 = ("14:30", "14:30")
    BLOCK_31 = ("15:00", "15:00")
    BLOCK_32 = ("15:30", "15:30")
    BLOCK_33 = ("16:00", "16:00")
    BLOCK_34 = ("16:30", "16:30")
    BLOCK_35 = ("17:00", "17:00")
    BLOCK_36 = ("17:30", "17:30")
    BLOCK_37 = ("18:00", "18:00")
    BLOCK_38 = ("18:30", "18:30")
    BLOCK_39 = ("19:00", "19:00")
    BLOCK_40 = ("19:30", "19:30")
    BLOCK_41 = ("20:00", "20:00")
    BLOCK_42 = ("20:30", "20:30")
    BLOCK_43 = ("21:00", "21:00")
    BLOCK_44 = ("21:30", "21:30")
    BLOCK_45 = ("22:00", "22:00")
    BLOCK_46 = ("22:30", "22:30")
    BLOCK_47 = ("23:00", "23:00")
    BLOCK_48 = ("23:30", "23:30")


class Consultation(models.Model):
    """
    Model representing a consultation.
    """
    pdl_profile = models.ForeignKey(PDLProfile, on_delete=models.CASCADE)
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    location = models.ForeignKey(ConsultationLocation, on_delete=models.CASCADE)
    reason = models.ForeignKey(ConsultationReason, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='scheduled')
    consultation_date_date_only = models.DateField(default=None)
    consultation_time_block = models.CharField(max_length=20, choices=[(block.name, block.value[1]) for block in ConsultationTimeBlock], default=ConsultationTimeBlock.BLOCK_01.name)
    is_an_emergency = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consultation with {self.physician} on {self.consultation_date_date_only.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"
        ordering = ['consultation_date_date_only', 'consultation_time_block']
        
        # PDL Consultation Constraints, make sure that a PDL Profile can only have one consultation per time block on the same date
        constraints = [
            models.UniqueConstraint(fields=['pdl_profile', 'consultation_date_date_only', 'consultation_time_block'], name='unique_consultation_per_pdl_per_time_block')
        ]
        # Physician Consultation Constraints, make sure that a Physician can only have one consultation per time block on the same date
        constraints += [
            models.UniqueConstraint(fields=['physician', 'consultation_date_date_only', 'consultation_time_block'], name='unique_consultation_per_physician_per_time_block')
        ]
        # Location Consultation Constraints, make sure that a Location can only have one consultation per time block on the same date
        constraints += [
            models.UniqueConstraint(fields=['location', 'consultation_date_date_only', 'consultation_time_block'], name='unique_consultation_per_location_per_time_block')
        ]
      