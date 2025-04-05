from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class DetentionStatus(models.Model):
    status = models.CharField(_("Status"), max_length=100)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = _("Detention Status")
        verbose_name_plural = _("Detention Statuses")


class PDLProfile(models.Model):
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email"), unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = _("PDL Profile")
        verbose_name_plural = _("PDL Profiles")


class DetentionReason(models.Model):
    reason = models.CharField(_("Reason"), max_length=255)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.reason

    class Meta:
        verbose_name = _("Detention Reason")
        verbose_name_plural = _("Detention Reasons")


class DetentionInstance(models.Model):
    pdl_profile = models.ForeignKey(
        PDLProfile, 
        on_delete=models.CASCADE, 
        related_name='detention_instances',
        verbose_name=_("PDL Profile")
    )
    detention_term_length = models.IntegerField(_("Detention Term Length"), default=0)
    detention_status = models.ForeignKey(
        DetentionStatus, 
        on_delete=models.CASCADE, 
        related_name='detention_instances',
        verbose_name=_("Detention Status")
    )
    detention_start_date = models.DateField(_("Detention Start Date"))
    detention_end_date = models.DateField(_("Detention End Date"), blank=True, null=True)
    detention_reason = models.ForeignKey(
        DetentionReason, 
        on_delete=models.CASCADE, 
        related_name='detention_instances',
        verbose_name=_("Detention Reason")
    )
    notes = models.TextField(_("Notes"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)


    def __str__(self):
        return f"{self.pdl_profile} - {self.detention_status} - {self.detention_start_date}"
    
    class Meta:
        verbose_name = _("Detention Instance")
        verbose_name_plural = _("Detention Instances")
        ordering = ['-detention_start_date']

        