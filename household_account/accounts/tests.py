from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Family

class FamilyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Family.objects.create(family_name='Test Family')

    def test_family_name_label(self):
        family = Family.objects.get(id=1)
        field_label = family._meta.get_field('family_name').verbose_name
        self.assertEqual(field_label, '家名')

    def test_family_name_max_length(self):
        family = Family.objects.get(id=1)
        max_length = family._meta.get_field('family_name').max_length
        self.assertEqual(max_length, 150)

    def test_family_name_unique(self):
        family = Family.objects.get(id=1)
        unique = family._meta.get_field('family_name').unique
        self.assertTrue(unique)

    def test_family_str_representation(self):
        family = Family.objects.get(id=1)
        self.assertEqual(str(family), family.family_name)


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        User.objects.create(
                account_id='test_account_id',
                email='test@example.com',
                first_name='Test',
                is_superuser=False,
                is_staff=False
                )

    def test_account_id_label(self):
        user = get_user_model().objects.get(id=1)
        field_label = user._meta.get_field('account_id').verbose_name
        self.assertEqual(field_label, 'account_id')

    def test_account_id_max_length(self):
        user = get_user_model().objects.get(id=1)
        max_length = user._meta.get_field('account_id').max_length
        self.assertEqual(max_length, 10)

    def test_email_label(self):
        user = get_user_model().objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_email_unique(self):
        user = get_user_model().objects.get(id=1)
        unique = user._meta.get_field('email').unique
        self.assertTrue(unique)

    def test_first_name_label(self):
        user = get_user_model().objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, '名前')

    def test_first_name_max_length(self):
        user = get_user_model().objects.get(id=1)
        max_length = user._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)

    def test_family_name_label(self):
        user = get_user_model().objects.get(id=1)
        field_label = user._meta.get_field('family_name').verbose_name
        self.assertEqual(field_label, '家名')

    def test_family_name_null(self):
        user = get_user_model().objects.get(id=1)
        family_name = user.family_name
        self.assertIsNone(family_name)

    def test_is_superuser_default(self):
        user = get_user_model().objects.get(id=1)
        is_superuser = user.is_superuser
        self.assertFalse(is_superuser)

    def test_is_staff_default(self):
        user = get_user_model().objects.get(id=1)
        is_staff = user.is_staff
        self.assertFalse(is_staff)
