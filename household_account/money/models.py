from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User

# 支出カテゴリ
class PaymentCategory(models.Model):
    name = models.CharField('支出カテゴリ', max_length=32)

    def __str__(self):
        return self.name

# 支出項目
class PaymentItem(models.Model):
    name = models.CharField('支出項目', max_length=32)
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')

    def __str__(self):
        return self.name

# ユーザー設定支出項目
class PaymentOrigItem(models.Model):
    account_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField('支出項目', max_length=32)
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')

    def __str__(self):
        return self.name

# 支出
class Payment(models.Model):
    account_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(PaymentItem, verbose_name='支出項目', on_delete=models.SET_NULL, null=True, blank=True)
    user_item = models.ForeignKey(PaymentOrigItem, verbose_name='ユーザー設定支出項目', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField('日付')
    price = models.IntegerField('金額')
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    description = models.TextField('備考', null=True, blank=True)

    def __str__(self):
        return f'{str(self.date)},{str(self.price)},{self.category}'

# 収入カテゴリ
class IncomeCategory(models.Model):
    name = models.CharField('収入カテゴリ', max_length=32)

    def __str__(self):
        return self.name

# 収入項目
class IncomeItem(models.Model):
    name = models.CharField('支出項目', max_length=32)
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')

    def __str__(self):
        return self.name

# ユーザー設定収入項目
class IncomeOrigItem(models.Model):
    account_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField('支出項目', max_length=32)
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')

    def __str__(self):
        return self.name

# 収入
class Income(models.Model):
    account_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(IncomeItem, verbose_name='支出項目', on_delete=models.SET_NULL, null=True, blank=True)
    user_item = models.ForeignKey(IncomeOrigItem, verbose_name='支出項目', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField('日付')
    price = models.IntegerField('金額')
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    description = models.TextField('備考', null=True, blank=True)

    def __str__(self):
        return f'{str(self.date)},{str(self.price)},{self.category}'

# 予算テーブル
class Budget(models.Model):
    year = models.IntegerField('年')
    month = models.IntegerField('月')
    budget_limit = models.IntegerField('月予算')
