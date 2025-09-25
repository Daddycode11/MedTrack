from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True, null=True)

     # --- Choices ---
    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    CIVIL_STATUS_CHOICES = [
        ("S", "Single"),
        ("M", "Married"),
        ("W", "Widowed"),
        ("D", "Divorced"),
        ("SEP", "Separated"),
        ("LI", "Live-in / Domestic partnership"),
    ]

    EDUCATION_CHOICES = [
        ("NONE", "No formal schooling"),
        ("ELEM", "Elementary"),
        ("HS", "High School"),
        ("SHS", "Senior High School"),
        ("VOC", "Vocational/Technical"),
        ("COL", "College/Undergraduate"),
        ("POST", "Postgraduate"),
    ]

    # --- Fields with verbose_name ---
    sex = models.CharField(
        "Sex",
        max_length=1,
        choices=SEX_CHOICES,
        blank=True,
        null=True
    )
    age = models.PositiveSmallIntegerField(
        "Age",
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        blank=True,
        null=True
    )
    civil_status = models.CharField(
        "Civil Status",
        max_length=3,
        choices=CIVIL_STATUS_CHOICES,
        blank=True,
        null=True
    )
    educational_attainment = models.CharField(
        "Educational Attainment",
        max_length=5,
        choices=EDUCATION_CHOICES,
        blank=True,
        null=True
    )
    date_of_birth = models.DateField("Date of Birth", blank=True, null=True)
    place_of_birth = models.CharField("Place of Birth", max_length=255, blank=True)

    place_of_birth_municipality = models.CharField("Municipality", max_length=128, blank=True)
    place_of_birth_province = models.CharField("Province", max_length=128, blank=True)
    place_of_birth_region = models.CharField("Region", max_length=128, blank=True)
    place_of_birth_country = models.CharField("Country", max_length=128, blank=True)

    date_of_commitment = models.DateField("Date of Commitment", blank=True, null=True)
    name_of_jail = models.CharField("Name of Jail", max_length=255, blank=True)

    case = models.CharField("Case", max_length=255, blank=True)
    case_number = models.CharField("Case Number", max_length=128, blank=True, db_index=True)

    origin_lockup = models.CharField("Origin Lockup", max_length=255, blank=True)

    contact_person_name = models.CharField("Name of Contact Person", max_length=255, blank=True)
    contact_person_address = models.TextField("Address of Contact Person", blank=True)
    contact_person_phone = models.CharField("Phone of Contact Person", max_length=64, blank=True)
    contact_person_email = models.EmailField("Email of Contact Person", blank=True)
    contact_person_relationship = models.CharField("Relationship to Contact Person", max_length=128, blank=True)




    def __str__(self):
        return f"{self.username.first_name} {self.username.last_name}"
    
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
    detention_room_number = models.CharField(_("Detention Room Number"), blank=True, null=True)
    detention_term_length = models.IntegerField(_("Detention Term Length"), default=0, blank=True, null=True)
    detention_status = models.ForeignKey(
        DetentionStatus, 
        on_delete=models.CASCADE, 
        related_name='detention_instances',
        verbose_name=_("Detention Status"),
        blank=True, null=True
    )
    detention_start_date = models.DateField(_("Detention Start Date"),blank=True, null=True)
    detention_end_date = models.DateField(_("Detention End Date"), blank=True, null=True)
    detention_reason = models.ForeignKey(
        DetentionReason, 
        on_delete=models.CASCADE, 
        related_name='detention_instances',
        verbose_name=_("Detention Reason"),
        blank=True, null=True
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

        