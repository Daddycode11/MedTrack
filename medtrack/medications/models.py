from django.db import models
from django.contrib.auth.models import User
from pdl.models import PDLProfile
from consultations.models import Physician

# Create your models here.

class Pharmacist(models.Model):
    """
    Model representing a pharmacist.
    """
    EMPLOYEE_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
    ]

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE_CHOICES, default='full_time')
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username.first_name} {self.username.last_name}"
    
class MedicationType(models.Model):
    """
    Model representing a type of medication.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Medication Type"
        verbose_name_plural = "Medication Types"
        ordering = ['name']

class MedicationGenericName(models.Model):
    """
    Model representing a generic name of a medication.
    """
    name = models.CharField(max_length=100)
    medication_type = models.ForeignKey(MedicationType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Medication Generic Name"
        verbose_name_plural = "Medication Generic Names"
        ordering = ['name']

class Medication(models.Model):
    """
    Model representing a medication.
    """
    DOSAGE_FORM_CHOICES = [
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream'),
        ('ointment', 'Ointment'),
    ]
    ROUTE_OF_ADMINISTRATION_CHOICES = [
        ('oral', 'Oral'),
        ('intravenous', 'Intravenous'),
        ('intramuscular', 'Intramuscular'),
        ('subcutaneous', 'Subcutaneous'),
        ('topical', 'Topical'),
    ]
    name = models.CharField(max_length=100)
    generic_name = models.ForeignKey(MedicationGenericName, on_delete=models.CASCADE)
    dosage_form = models.CharField(max_length=20, choices=DOSAGE_FORM_CHOICES)
    strength = models.CharField(max_length=50)
    route_of_administration = models.CharField(max_length=20, choices=ROUTE_OF_ADMINISTRATION_CHOICES)
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.generic_name})"
    
    class Meta:
        verbose_name = "Medication"
        verbose_name_plural = "Medications"
        ordering = ['name']


class MedicationInventory(models.Model):
    """
    Model representing the inventory of medications.
    """
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    expiration_date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medication} - {self.quantity} units"
    
    class Meta:
        verbose_name = "Medication Inventory"
        verbose_name_plural = "Medication Inventories"
        ordering = ['medication__name']


class MedicationPrescription(models.Model):
    """
    Model representing a medication prescription.
    """
    pdl_profile = models.ForeignKey(PDLProfile, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    prescribed_by = models.ForeignKey(Physician, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.medication} prescribed to {self.pdl_profile}"
    
    class Meta:
        verbose_name = "Medication Prescription"
        verbose_name_plural = "Medication Prescriptions"
        ordering = ['pdl_profile__username__last_name']