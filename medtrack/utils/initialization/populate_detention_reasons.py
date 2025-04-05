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