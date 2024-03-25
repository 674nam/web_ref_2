from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import PaymentCategory, IncomeCategory,\
                    PaymentItem, IncomeItem,\
                    PaymentOrigItem, IncomeOrigItem,\
                    Payment, Income

class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
                        account_id='test_account_id',
                        email='test@example.com',
                        first_name='Test',
                        is_superuser=False,
                        is_staff=False
                        )
        cls.payment_category = PaymentCategory.objects.create(
                        name='Test Payment Category'
                        )
        cls.income_category = IncomeCategory.objects.create(
                        name='Test Income Category'
                        )
        cls.payment_item = PaymentItem.objects.create(
                        name='Test Payment Item',
                        category=cls.payment_category
                        )
        cls.income_item = IncomeItem.objects.create(
                        name='Test Income Item',
                        category=cls.income_category
                        )
        cls.payment_orig_item = PaymentOrigItem.objects.create(
                        account_id=cls.user,
                        name='Test Payment Orig Item',
                        category=cls.payment_category
                        )
        cls.income_orig_item = IncomeOrigItem.objects.create(
                        account_id=cls.user,
                        name='Test Income Orig Item',
                        category=cls.income_category
                        )
        cls.payment = Payment.objects.create(
                        date='2024-03-25',
                        account_id=cls.user,
                        category=cls.payment_category,
                        item=cls.payment_item,
                        user_item=cls.payment_orig_item,
                        price=100,
                        description='Test Payment'
                        )
        cls.income = Income.objects.create(
                        date='2024-03-25',
                        account_id=cls.user,
                        category=cls.income_category,
                        item=cls.income_item,
                        user_item=cls.income_orig_item,
                        price=100,
                        description='Test Income'
                        )

    def test_payment_category_str(self):
        category = PaymentCategory.objects.get(id=1)
        self.assertEqual(str(category), 'Test Payment Category')

    def test_income_category_str(self):
        category = IncomeCategory.objects.get(id=1)
        self.assertEqual(str(category), 'Test Income Category')

    def test_payment_item_str(self):
        item = PaymentItem.objects.get(id=1)
        self.assertEqual(str(item), f'{self.payment_category} ; Test Payment Item')

    def test_income_item_str(self):
        item = IncomeItem.objects.get(id=1)
        self.assertEqual(str(item), f'{self.income_category} ; Test Income Item')

    def test_payment_orig_item_str(self):
        item = PaymentOrigItem.objects.get(id=1)
        self.assertEqual(str(item), f'{self.payment_category} ; Test Payment Orig Item')

    def test_income_orig_item_str(self):
        item = IncomeOrigItem.objects.get(id=1)
        self.assertEqual(str(item), f'{self.income_category} ; Test Income Orig Item')

    def test_payment_str(self):
        payment = Payment.objects.get(id=1)
        self.assertEqual(str(payment), '2024-03-25,100,Test Payment Category')

    def test_income_str(self):
        income = Income.objects.get(id=1)
        self.assertEqual(str(income), '2024-03-25,100,Test Income Category')
