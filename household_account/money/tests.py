from django.test import TestCase
from django.utils import timezone
from .models import PaymentCategory, IncomeCategory \
                    , PaymentItem, IncomeItem \
                    , PaymentOrigItem, IncomeOrigItem \
                    , Payment, Income
from django.contrib.auth import get_user_model

class MoneyTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.test_user = User.objects.create(account_id="test_account",
                                            email="test@example.com",
                                            first_name="Test",
                                            is_superuser=False,
                                            is_staff=False)

    @classmethod
    def create_payment_category(self):
        return PaymentCategory.objects.create(name="Test Payment Category")

    @classmethod
    def create_income_category(self):
        return IncomeCategory.objects.create(name="Test Income Category")

    @classmethod
    def create_payment_item(self, category):
        return PaymentItem.objects.create(name="Test Payment Item", category=category)

    @classmethod
    def create_income_item(self, category):
        return IncomeItem.objects.create(name="Test Income Item", category=category)

    @classmethod
    def create_payment_orig_item(self, category):
        return PaymentOrigItem.objects.create(name="Test User Payment Item", category=category, account_id=self.test_user)

    @classmethod
    def create_income_orig_item(self, category):
        return IncomeOrigItem.objects.create(name="Test User Income Item", category=category, account_id=self.test_user)

    @classmethod
    def create_payment(self, category, item):
        return Payment.objects.create(date=timezone.now(), account_id=self.test_user, category=category, item=item, price=100)

    @classmethod
    def create_income(self, category, item):
        return Income.objects.create(date=timezone.now(), account_id=self.test_user, category=category, item=item, price=100)

    def test_check(self):
        payment_category = self.create_payment_category()
        self.assertEqual(str(payment_category), "Test Payment Category")

        income_category = self.create_income_category()
        self.assertEqual(str(income_category), "Test Income Category")

        payment_item = self.create_payment_item(payment_category)
        self.assertEqual(str(payment_item), f'{payment_category} ; Test Payment Item')

        income_item = self.create_income_item(income_category)
        self.assertEqual(str(income_item), f'{income_category} ; Test Income Item')

        payment_orig_item = self.create_payment_orig_item(payment_category)
        self.assertEqual(str(payment_orig_item), f'{payment_category} ; Test User Payment Item')

        income_orig_item = self.create_income_orig_item(income_category)
        self.assertEqual(str(income_orig_item), f'{income_category} ; Test User Income Item')

        payment = self.create_payment(payment_category, payment_item)
        self.assertEqual(str(payment), f'{str(payment.date)},{str(payment.price)},{payment.category}')

        income = self.create_income(income_category, income_item)
        self.assertEqual(str(income), f'{str(income.date)},{str(income.price)},{income.category}')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()