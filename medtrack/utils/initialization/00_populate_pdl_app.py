## PART 1 : DETENTION REASONS

from pdl.models import DetentionReason

# Suggested detention reasons
detention_reasons = [
    {"reason": "Theft", "description": "Unlawful taking of another's property."},
    {"reason": "Assault", "description": "Physical attack or threat of attack."},
    {"reason": "Drug Possession", "description": "Possession of illegal substances."},
    {"reason": "Fraud", "description": "Deception for personal or financial gain."},
    {"reason": "Vandalism", "description": "Deliberate destruction of property."},
    {"reason": "Trespassing", "description": "Unauthorized entry onto private property."},
    {"reason": "Domestic Violence", "description": "Violence or abuse within a household."},
    {"reason": "Public Intoxication", "description": "Being drunk in a public place."},
    {"reason": "Disorderly Conduct", "description": "Disruptive or offensive behavior in public."},
    {"reason": "Burglary", "description": "Illegal entry into a building with intent to commit a crime."},
]

# Delete existing records
DetentionReason.objects.all().delete()

# Populate the database
for reason_data in detention_reasons:
    reason, created = DetentionReason.objects.get_or_create(
        reason=reason_data["reason"],
        defaults={"description": reason_data["description"]}
    )
    if created:
        print(f"Added detention reason: {reason.reason}")
    else:
        print(f"Detention reason already exists: {reason.reason}")


## PART 2 : DETENTION TYPES
from pdl.models import DetentionStatus

# Suggested detention statuses
detention_statuses = [
    {"status": "In Custody", "description": "Currently detained in a facility."},
    {"status": "Released", "description": "No longer in custody."},
    {"status": "Transferred", "description": "Moved to another facility or jurisdiction."},
    {"status": "On Bail", "description": "Released temporarily on bail."},
    {"status": "Escaped", "description": "Unlawfully left custody."},
    {"status": "Under Investigation", "description": "Being investigated but not yet detained."},
]

# Delete existing records
DetentionStatus.objects.all().delete()

# Populate the database
for status_data in detention_statuses:
    status, created = DetentionStatus.objects.get_or_create(
        status=status_data["status"],
        defaults={"description": status_data["description"]}
    )
    if created:
        print(f"Added detention status: {status.status}")
    else:
        print(f"Detention status already exists: {status.status}")

## PART 3 : PDL Profiles

from pdl.models import PDLProfile

# Suggested PDL profiles
pdl_names = [
    {"first_name": "John", "last_name": "Doe", "email": "johndoe@email.com", "phone_number": "1234567890"},
    {"first_name": "Jane", "last_name": "Smith", "email": "janesmith@email.com", "phone_number": "9876543210"},
    {"first_name": "Michael", "last_name": "Johnson", "email": "michaeljohnson@email.com", "phone_number": "5551234567"},
    {"first_name": "Emily", "last_name": "Davis", "email": "emilydavis@email.com", "phone_number": "4449876543"},
    {"first_name": "Chris", "last_name": "Brown", "email": "chrisbrown@email.com", "phone_number": "3334567890"},
    {"first_name": "Sarah", "last_name": "Wilson", "email": "sarahwilson@email.com", "phone_number": "2221239876"},
    {"first_name": "David", "last_name": "Martinez", "email": "davidmartinez@email.com", "phone_number": "1119876543"},
    {"first_name": "Laura", "last_name": "Garcia", "email": "lauragarcia@email.com", "phone_number": "6667891234"},
    {"first_name": "James", "last_name": "Anderson", "email": "jamesanderson@email.com", "phone_number": "7776543210"},
    {"first_name": "Olivia", "last_name": "Taylor", "email": "oliviataylor@email.com", "phone_number": "8881234567"},
    {"first_name": "Daniel", "last_name": "Thomas", "email": "danielthomas@email.com", "phone_number": "9999876543"},
]

# Delete existing records
PDLProfile.objects.all().delete()
# Populate the database
for pdl_data in pdl_names:
    pdl_profile, created = PDLProfile.objects.get_or_create(
        first_name=pdl_data["first_name"],
        last_name=pdl_data["last_name"],
        defaults={
            "email": pdl_data["email"],
            "phone_number": pdl_data["phone_number"]
        }
    )
    if created:
        print(f"Added PDL profile: {pdl_profile.first_name} {pdl_profile.last_name}")
    else:
        print(f"PDL profile already exists: {pdl_profile.first_name} {pdl_profile.last_name}")


## PART 4 : DETENTION INSTANCES
from pdl.models import DetentionInstance
from datetime import datetime, timedelta
import random

# Suggested detention instances
detention_instances = [
    {
        "pdl_profile": PDLProfile.objects.get(first_name="John", last_name="Doe"),
        "detention_term_length": 30,
        "detention_status": DetentionStatus.objects.get(status="In Custody"),
        "detention_start_date": datetime.now() - timedelta(days=10),
        "detention_end_date": None,
        "detention_reason": DetentionReason.objects.get(reason="Theft")
    },
    {
        "pdl_profile": PDLProfile.objects.get(first_name="Jane", last_name="Smith"),
        "detention_term_length": 60,
        "detention_status": DetentionStatus.objects.get(status="Released"),
        "detention_start_date": datetime.now() - timedelta(days=70),
        "detention_end_date": datetime.now() - timedelta(days=10),
        "detention_reason": DetentionReason.objects.get(reason="Assault")
    },
    {
        "pdl_profile": PDLProfile.objects.get(first_name="Michael", last_name="Johnson"),
        "detention_term_length": 90,
        "detention_status": DetentionStatus.objects.get(status="Transferred"),
        "detention_start_date": datetime.now() - timedelta(days=50),
        "detention_end_date": None,
        "detention_reason": DetentionReason.objects.get(reason="Drug Possession")
    },
    {
        "pdl_profile": PDLProfile.objects.get(first_name="Emily", last_name="Davis"),
        "detention_term_length": 45,
        "detention_status": DetentionStatus.objects.get(status="On Bail"),
        "detention_start_date": datetime.now() - timedelta(days=20),
        "detention_end_date": None,
        "detention_reason": DetentionReason.objects.get(reason="Fraud")
    },
    {
        "pdl_profile": PDLProfile.objects.get(first_name="Chris", last_name="Brown"),
        "detention_term_length": 120,
        "detention_status": DetentionStatus.objects.get(status="Escaped"),
        "detention_start_date": datetime.now() - timedelta(days=150),
        "detention_end_date": None,
        "detention_reason": DetentionReason.objects.get(reason="Vandalism")
    },
    {
        "pdl_profile": PDLProfile.objects.get(first_name="Sarah", last_name="Wilson"),
        "detention_term_length": 15,
        "detention_status": DetentionStatus.objects.get(status="Under Investigation"),
        "detention_start_date": datetime.now() - timedelta(days=5),
        "detention_end_date": None,
        "detention_reason": DetentionReason.objects.get(reason="Trespassing")
    },
    {
        "pdl_profile": PDLProfile.objects.get(first_name="David", last_name="Martinez"),
        "detention_term_length": 60,
        "detention_status": DetentionStatus.objects.get(status="In Custody"),
        "detention_start_date": datetime.now() - timedelta(days=30),
        "detention_end_date": None,
        "detention_reason": DetentionReason.objects.get(reason="Domestic Violence")
    },
    {
        "pdl_profile": PDLProfile.objects.get(first_name="Laura", last_name="Garcia"),
        "detention_term_length": 10,
        "detention_status": DetentionStatus.objects.get(status="Released"),
        "detention_start_date": datetime.now() - timedelta(days=15),
        "detention_end_date": datetime.now() - timedelta(days=5),
        "detention_reason": DetentionReason.objects.get(reason="Public Intoxication")
    },
    {
        "pdl_profile": PDLProfile.objects.get(first_name="James", last_name="Anderson"),
        "detention_term_length": 25,
        "detention_status": DetentionStatus.objects.get(status="Transferred"),
        "detention_start_date": datetime.now() - timedelta(days=40),
        "detention_end_date": None,
        "detention_reason": DetentionReason.objects.get(reason="Disorderly Conduct")
    },
    {
        "pdl_profile": PDLProfile.objects.get(first_name="Olivia", last_name="Taylor"),
        "detention_term_length": 90,
        "detention_status": DetentionStatus.objects.get(status="On Bail"),
        "detention_start_date": datetime.now() - timedelta(days=60),
        "detention_end_date": None,
        "detention_reason": DetentionReason.objects.get(reason="Burglary")
    },
]

# Delete existing records
DetentionInstance.objects.all().delete()

# Populate the database
for instance_data in detention_instances:
    instance, created = DetentionInstance.objects.get_or_create(
        pdl_profile=instance_data["pdl_profile"],
        detention_term_length=instance_data["detention_term_length"],
        detention_status=instance_data["detention_status"],
        detention_start_date=instance_data["detention_start_date"],
        detention_end_date=instance_data["detention_end_date"],
        detention_reason=instance_data["detention_reason"]
    )
    if created:
        print(f"Added detention instance for: {instance.pdl_profile.first_name} {instance.pdl_profile.last_name}")
    else:
        print(f"Detention instance already exists for: {instance.pdl_profile.first_name} {instance.pdl_profile.last_name}")
        