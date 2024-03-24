from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Family

class FamilyTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_family_name = "Test Family"
        cls.family = Family.objects.create(family_name=cls.test_family_name)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_check_family(self):
        self.assertEqual(str(self.family), f'{str(self.family.id)} , {self.test_family_name}')
        self.assertEqual(self.family.family_name, self.test_family_name)


class UserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.test_user_account_id = "test_account"
        cls.test_user_email = "test@example.com"
        cls.test_user_first_name = "Test"
        cls.test_family = Family.objects.create(family_name="Test Family")
        cls.test_user = User.objects.create(account_id=cls.test_user_account_id, email=cls.test_user_email, first_name=cls.test_user_first_name, family_name=cls.test_family)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_check_user(self):
        self.assertEqual(self.test_user.account_id, self.test_user_account_id)
        self.assertEqual(self.test_user.email, self.test_user_email)
        self.assertEqual(self.test_user.first_name, self.test_user_first_name)
        self.assertEqual(str(self.test_user.family_name), f'{str(self.test_family.id)} , {self.test_family.family_name}')
