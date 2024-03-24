from django.db import models
from accounts.models import User

# 支出カテゴリ
class PaymentCategory(models.Model):
    name = models.CharField('支出カテゴリ', max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)

# 収入カテゴリ
class IncomeCategory(models.Model):
    name = models.CharField('収入カテゴリ', max_length=32, unique=True,)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)

# 支出項目
class PaymentItem(models.Model):
    name = models.CharField('支出項目', max_length=32, unique=True)
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')

    def __str__(self):
        return f'{self.category} ; {self.name}'

    class Meta:
        ordering = ('id',)

# 収入項目
class IncomeItem(models.Model):
    name = models.CharField('収入項目', max_length=32, unique=True)
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')

    def __str__(self):
        return f'{self.category} ; {self.name}'

    class Meta:
        ordering = ('id',)

# ユーザー設定支出項目
class PaymentOrigItem(models.Model):
    account_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField('ユーザー設定支出項目', max_length=32)
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')

    def __str__(self):
        return f'{self.category} ; {self.name}'
    class Meta:
        ordering = ('category',)

# ユーザー設定収入項目
class IncomeOrigItem(models.Model):
    account_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField('ユーザー設定収入項目', max_length=32)
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')

    def __str__(self):
        return f'{self.category} ; {self.name}'

    class Meta:
        ordering = ('category',)

# 支出
class Payment(models.Model):
    date = models.DateField('日付')
    account_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    item = models.ForeignKey(PaymentItem, verbose_name='支出項目', on_delete=models.SET_NULL, null=True, blank=True)
    user_item = models.ForeignKey(PaymentOrigItem, verbose_name='ユーザー設定支出項目', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField('金額')
    description = models.TextField('備考', null=True, blank=True)

    def __str__(self):
        return f'{str(self.date)},{str(self.price)},{self.category}'

    class Meta:
        ordering = ('-date',)

# 収入
class Income(models.Model):
    date = models.DateField('日付')
    account_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(IncomeCategory, on_delete=models.PROTECT, verbose_name='カテゴリ')
    item = models.ForeignKey(IncomeItem, verbose_name='収入項目', on_delete=models.SET_NULL, null=True, blank=True)
    user_item = models.ForeignKey(IncomeOrigItem, verbose_name='ユーザー設定収入項目', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField('金額')
    description = models.TextField('備考', null=True, blank=True)

    def __str__(self):
        return f'{str(self.date)},{str(self.price)},{self.category}'

    class Meta:
        ordering = ('-date',)

# 予算テーブル
class Budget(models.Model):
    year = models.IntegerField('年')
    month = models.IntegerField('月')
    budget_limit = models.IntegerField('月予算')

    class Meta:
        ordering = ('-month',)
