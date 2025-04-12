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
    BLOCK_08_00 = ("08:00", "8:00 AM")
    BLOCK_08_30 = ("08:30", "8:30 AM")
    BLOCK_09_00 = ("09:00", "9:00 AM")
    BLOCK_09_30 = ("09:30", "9:30 AM")
    BLOCK_10_00 = ("10:00", "10:00 AM")
    BLOCK_10_30 = ("10:30", "10:30 AM")
    BLOCK_11_00 = ("11:00", "11:00 AM")
    BLOCK_11_30 = ("11:30", "11:30 AM")
    BLOCK_13_00 = ("13:00", "1:00 PM")
    BLOCK_13_30 = ("13:30", "1:30 PM")
    BLOCK_14_00 = ("14:00", "2:00 PM")
    BLOCK_14_30 = ("14:30", "2:30 PM")
    BLOCK_15_00 = ("15:00", "3:00 PM")
    BLOCK_15_30 = ("15:30", "3:30 PM")
    BLOCK_16_00 = ("16:00", "4:00 PM")
    BLOCK_16_30 = ("16:30", "4:30 PM")
    BLOCK_17_00 = ("17:00", "5:00 PM")

    @classmethod
    def get_block_by_time(cls, time_str):
        """Get enum member by time string."""
        for block in cls:
            if block.value[0] == time_str:
                return block.name
        return None

    @classmethod
    def get_display_time(cls, block_name):
        """Get display time from block name."""
        try:
            return cls[block_name].value[1]
        except KeyError:
            return None

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
    consultation_time_block = models.CharField(
        max_length=20, 
        choices=[(block.name, block.value[1]) for block in ConsultationTimeBlock],
        default=ConsultationTimeBlock.BLOCK_08_00.name  # Change this line
    )
    is_an_emergency = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        # Consultation with Physician on Month Year, Time Block
        # lookup block name in enum
        block_name = self.consultation_time_block
        block_value = ConsultationTimeBlock[block_name].value[1]
        return f"Consultation with {self.physician} on {self.consultation_date_date_only.strftime('%d %B %Y')} at {block_value} in {self.location.room_number}"
    
    @property
    def consultation_time_block_display(self):
        """
        Returns the display value of the consultation time block.
        """
        return ConsultationTimeBlock[self.consultation_time_block].value[1]
    
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
      