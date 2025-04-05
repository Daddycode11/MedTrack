from django.test import TestCase
from django.contrib.auth.models import User
from .models import DetentionStatus, PDLProfile, DetentionReason, DetentionInstance
from datetime import datetime, timedelta

class DetentionStatusModelTest(TestCase):
    def setUp(self):
        self.status = DetentionStatus.objects.create(
            status="In Custody",
            description="Currently detained in a facility."
        )

    def test_str_representation(self):
        self.assertEqual(str(self.status), "In Custody")

    def test_verbose_name(self):
        self.assertEqual(self.status._meta.verbose_name, "Detention Status")

    def test_verbose_name_plural(self):
        self.assertEqual(self.status._meta.verbose_name_plural, "Detention Statuses")


class PDLProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="johndoe",
            email="johndoe@email.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.pdl = PDLProfile.objects.create(
            username=self.user,
            phone_number="1234567890"
        )

    def test_str_representation(self):
        self.assertEqual(str(self.pdl), "John Doe")



class DetentionReasonModelTest(TestCase):
    def setUp(self):
        self.reason = DetentionReason.objects.create(
            reason="Theft",
            description="Unlawful taking of another's property."
        )

    def test_str_representation(self):
        self.assertEqual(str(self.reason), "Theft")


class DetentionInstanceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            email="johndoe@email.com",
            password="password123"
        )
        self.pdl = PDLProfile.objects.create(
            username=self.user,
            phone_number="1234567890"
        )
        self.status = DetentionStatus.objects.create(
            status="In Custody",
            description="Currently detained in a facility."
        )
        self.reason = DetentionReason.objects.create(
            reason="Theft",
            description="Unlawful taking of another's property."
        )
        self.instance = DetentionInstance.objects.create(
            pdl_profile=self.pdl,
            detention_term_length=30,
            detention_status=self.status,
            detention_start_date=datetime.now() - timedelta(days=10),
            detention_end_date=None,
            detention_reason=self.reason,
            notes="First offense."
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.instance),
            f"{self.pdl} - {self.status} - {self.instance.detention_start_date}"
        )

    def test_ordering(self):
        instances = DetentionInstance.objects.all()
        self.assertEqual(instances[0], self.instance)
