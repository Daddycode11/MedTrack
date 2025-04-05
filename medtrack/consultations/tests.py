from django.test import TestCase
from django.db.utils import IntegrityError
from .models import (
    MedicalSpecialty,
    Physician,
    ConsultationLocation,
    ConsultationReason,
    Consultation,
    ConsultationTimeBlock,
)
import datetime as dt
from pdl.models import PDLProfile  # Ensure this is correctly imported or mocked

class MedicalSpecialtyModelTest(TestCase):
    def setUp(self):
        self.specialty = MedicalSpecialty.objects.create(
            name="Cardiology",
            description="Heart-related medical specialty."
        )

    def test_medical_specialty_creation(self):
        self.assertEqual(self.specialty.name, "Cardiology")
        self.assertEqual(self.specialty.description, "Heart-related medical specialty.")

    def test_medical_specialty_str(self):
        self.assertEqual(str(self.specialty), "Cardiology")


class PhysicianModelTest(TestCase):
    def setUp(self):
        self.specialty = MedicalSpecialty.objects.create(name="Neurology", description="Brain-related specialty.")
        self.physician = Physician.objects.create(
            first_name="John",
            last_name="Doe",
            employee_type="full_time",
            specialty=self.specialty,
            phone_number="1234567890",
            email="johndoe@example.com",
            address="123 Main St"
        )

    def test_physician_creation(self):
        self.assertEqual(self.physician.first_name, "John")
        self.assertEqual(self.physician.last_name, "Doe")
        self.assertEqual(self.physician.specialty, self.specialty)

    def test_physician_str(self):
        self.assertEqual(str(self.physician), "John Doe (Neurology)")


class ConsultationLocationModelTest(TestCase):
    def setUp(self):
        self.location = ConsultationLocation.objects.create(
            room_number="101",
            capacity=10
        )

    def test_consultation_location_creation(self):
        self.assertEqual(self.location.room_number, "101")
        self.assertEqual(self.location.capacity, 10)

    def test_consultation_location_str(self):
        self.assertEqual(str(self.location), "101")


class ConsultationReasonModelTest(TestCase):
    def setUp(self):
        self.reason = ConsultationReason.objects.create(
            reason="Routine Checkup",
            description="A regular health checkup."
        )

    def test_consultation_reason_creation(self):
        self.assertEqual(self.reason.reason, "Routine Checkup")
        self.assertEqual(self.reason.description, "A regular health checkup.")

    def test_consultation_reason_str(self):
        self.assertEqual(str(self.reason), "Routine Checkup")


class ConsultationModelTest(TestCase):
    def setUp(self):
        self.specialty = MedicalSpecialty.objects.create(name="Dermatology", description="Skin-related specialty.")
        self.physician = Physician.objects.create(
            first_name="Alice",
            last_name="Smith",
            employee_type="part_time",
            specialty=self.specialty,
            phone_number="9876543210",
            email="alicesmith@example.com",
            address="456 Elm St"
        )
        self.location = ConsultationLocation.objects.create(room_number="202", capacity=5)
        self.reason = ConsultationReason.objects.create(reason="Skin Rash", description="Consultation for skin rash.")
        self.pdl_profile = PDLProfile.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com",
            phone_number="5551234567"
        )
                                    
        self.consultation = Consultation.objects.create(
            pdl_profile=self.pdl_profile,
            physician=self.physician,
            location=self.location,
            reason=self.reason,
            status="scheduled",
            consultation_date_date_only=dt.datetime(2025, 4, 5),
            consultation_time_block=ConsultationTimeBlock.BLOCK_17.name,
            is_an_emergency=False,
            notes="Patient has mild symptoms."
        )

    def test_consultation_creation(self):
        self.assertEqual(self.consultation.physician, self.physician)
        self.assertEqual(self.consultation.location, self.location)
        self.assertEqual(self.consultation.reason, self.reason)
        self.assertEqual(self.consultation.status, "scheduled")
        self.assertEqual(self.consultation.consultation_date_date_only.strftime('%Y-%m-%d'), "2025-04-05")
        self.assertEqual(self.consultation.consultation_time_block, ConsultationTimeBlock.BLOCK_17.name)
        self.assertFalse(self.consultation.is_an_emergency)
        self.assertEqual(self.consultation.notes, "Patient has mild symptoms.")

    def test_consultation_str(self):
        self.assertEqual(
            str(self.consultation),
            f"Consultation with {self.physician} on 2025-04-05"
        )

    def test_unique_constraints(self):
        # Test PDLProfile unique constraint
        with self.assertRaises(IntegrityError):
            Consultation.objects.create(
                pdl_profile=self.pdl_profile,
                physician=self.physician,
                location=self.location,
                reason=self.reason,
                status="scheduled",
                consultation_date_date_only="2025-04-05",
                consultation_time_block=ConsultationTimeBlock.BLOCK_17.name,
                is_an_emergency=False,
                notes="Duplicate consultation."
            )
