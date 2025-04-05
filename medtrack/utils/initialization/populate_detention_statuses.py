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