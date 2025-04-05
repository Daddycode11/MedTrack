from django.test import TestCase
from django.contrib.auth.models import User
from pdl.models import PDLProfile
from consultations.models import (
    Physician,
    MedicalSpecialty
)

from .models import (
    Pharmacist,
    MedicationType,
    MedicationGenericName,
    Medication,
    MedicationInventory,
    MedicationPrescription,
)
from datetime import date, timedelta


class PharmacistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="pharmacist1", first_name="John", last_name="Doe Pharmacist")
        self.pharmacist = Pharmacist.objects.create(
            username=self.user,
            employee_type="full_time",
            phone_number="1234567890",
            address="123 Main St"
        )

    def test_pharmacist_creation(self):
        self.assertEqual(self.pharmacist.username.username, "pharmacist1")
        self.assertEqual(self.pharmacist.phone_number, "1234567890")
        self.assertEqual(self.pharmacist.address, "123 Main St")

    def test_pharmacist_str(self):
        self.assertEqual(str(self.pharmacist), "John Doe Pharmacist")


class MedicationTypeModelTest(TestCase):
    def setUp(self):
        self.medication_type = MedicationType.objects.create(name="Antibiotic")

    def test_medication_type_creation(self):
        self.assertEqual(self.medication_type.name, "Antibiotic")

    def test_medication_type_str(self):
        self.assertEqual(str(self.medication_type), "Antibiotic")


class MedicationGenericNameModelTest(TestCase):
    def setUp(self):
        self.medication_type = MedicationType.objects.create(name="Antibiotic")
        self.generic_name = MedicationGenericName.objects.create(
            name="Amoxicillin",
            medication_type=self.medication_type
        )

    def test_generic_name_creation(self):
        self.assertEqual(self.generic_name.name, "Amoxicillin")
        self.assertEqual(self.generic_name.medication_type, self.medication_type)

    def test_generic_name_str(self):
        self.assertEqual(str(self.generic_name), "Amoxicillin")


class MedicationModelTest(TestCase):
    def setUp(self):
        self.medication_type = MedicationType.objects.create(name="Antibiotic")
        self.generic_name = MedicationGenericName.objects.create(
            name="Amoxicillin",
            medication_type=self.medication_type
        )
        self.medication = Medication.objects.create(
            name="Amoxil",
            generic_name=self.generic_name,
            dosage_form="tablet",
            strength="500mg",
            route_of_administration="oral",
            manufacturer="PharmaCorp"
        )

    def test_medication_creation(self):
        self.assertEqual(self.medication.name, "Amoxil")
        self.assertEqual(self.medication.generic_name, self.generic_name)
        self.assertEqual(self.medication.dosage_form, "tablet")
        self.assertEqual(self.medication.strength, "500mg")
        self.assertEqual(self.medication.route_of_administration, "oral")
        self.assertEqual(self.medication.manufacturer, "PharmaCorp")

    def test_medication_str(self):
        self.assertEqual(str(self.medication), "Amoxil (Amoxicillin)")


class MedicationInventoryModelTest(TestCase):
    def setUp(self):
        self.medication_type = MedicationType.objects.create(name="Antibiotic")
        self.generic_name = MedicationGenericName.objects.create(
            name="Amoxicillin",
            medication_type=self.medication_type
        )
        self.medication = Medication.objects.create(
            name="Amoxil",
            generic_name=self.generic_name,
            dosage_form="tablet",
            strength="500mg",
            route_of_administration="oral",
            manufacturer="PharmaCorp"
        )
        self.inventory = MedicationInventory.objects.create(
            medication=self.medication,
            quantity=100,
            expiration_date=date.today() + timedelta(days=365),
            location="Warehouse A"
        )

    def test_inventory_creation(self):
        self.assertEqual(self.inventory.medication, self.medication)
        self.assertEqual(self.inventory.quantity, 100)
        self.assertEqual(self.inventory.location, "Warehouse A")

    def test_inventory_str(self):
        self.assertEqual(str(self.inventory), "Amoxil (Amoxicillin) - 100 units")


class MedicationPrescriptionModelTest(TestCase):
    def setUp(self):
        self.user_pdl = User.objects.create_user(username="janedoe", first_name="Jane", last_name="Doe")
        self.pdl_profile = PDLProfile.objects.create(username=self.user_pdl, phone_number="5551234567")

        self.user_physician = User.objects.create_user(username="drsmithdoctor", first_name="John", last_name="Smith Doctor")
        self.physician = Physician.objects.create(
            username=self.user_physician,
            employee_type="full_time",
            specialty=MedicalSpecialty.objects.create(name="Cardiology", description="Heart-related medical specialty."),
            phone_number="1234567890",
            address="123 Main St"
        )

        self.medication_type = MedicationType.objects.create(name="Antibiotic")
        self.generic_name = MedicationGenericName.objects.create(
            name="Amoxicillin",
            medication_type=self.medication_type
        )
        self.medication = Medication.objects.create(
            name="Amoxil",
            generic_name=self.generic_name,
            dosage_form="tablet",
            strength="500mg",
            route_of_administration="oral",
            manufacturer="PharmaCorp"
        )
        self.prescription = MedicationPrescription.objects.create(
            pdl_profile=self.pdl_profile,
            medication=self.medication,
            dosage="500mg",
            frequency="3 times a day",
            duration="7 days",
            prescribed_by=self.physician
        )

    def test_prescription_creation(self):
        self.assertEqual(self.prescription.pdl_profile, self.pdl_profile)
        self.assertEqual(self.prescription.medication, self.medication)
        self.assertEqual(self.prescription.dosage, "500mg")
        self.assertEqual(self.prescription.frequency, "3 times a day")
        self.assertEqual(self.prescription.duration, "7 days")
        self.assertEqual(self.prescription.prescribed_by, self.physician)

    def test_prescription_str(self):
        self.assertEqual(str(self.prescription), "Amoxil (Amoxicillin) prescribed to Jane Doe")
