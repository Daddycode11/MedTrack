from django.db import models

# Create your models here.
class DetentionStatus(models.Model):
    status = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Detention Status"
        verbose_name_plural = "Detention Statuses"


class PDLProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "PDL Profile"
        verbose_name_plural = "PDL Profiles"

class DetentionReason(models.Model):
    reason = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.reason

    class Meta:
        verbose_name = "Detention Reason"
        verbose_name_plural = "Detention Reasons"

class DetentionInstance(models.Model):
    pdl_profile = models.ForeignKey(PDLProfile, on_delete=models.CASCADE, related_name='detention_instances')
    detention_status = models.ForeignKey(DetentionStatus, on_delete=models.CASCADE, related_name='detention_instances')
    detention_start_date = models.DateField()
    detention_end_date = models.DateField(blank=True, null=True)
    detention_reason = models.ForeignKey(DetentionReason, on_delete=models.CASCADE, related_name='detention_instances')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   