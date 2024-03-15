# Generated by Django 4.2.2 on 2024-03-15 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='年')),
                ('month', models.IntegerField(verbose_name='月')),
                ('budget_limit', models.IntegerField(verbose_name='月予算')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='収入カテゴリ')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='支出カテゴリ')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentOrigItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='支出項目')),
                ('account_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.paymentcategory', verbose_name='カテゴリ')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='支出項目')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.paymentcategory', verbose_name='カテゴリ')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('price', models.IntegerField(verbose_name='金額')),
                ('description', models.TextField(blank=True, null=True, verbose_name='備考')),
                ('account_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.paymentcategory', verbose_name='カテゴリ')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='money.paymentitem', verbose_name='支出項目')),
                ('user_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='money.paymentorigitem', verbose_name='ユーザー設定支出項目')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeOrigItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='支出項目')),
                ('account_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.incomecategory', verbose_name='カテゴリ')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='支出項目')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.incomecategory', verbose_name='カテゴリ')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('price', models.IntegerField(verbose_name='金額')),
                ('description', models.TextField(blank=True, null=True, verbose_name='備考')),
                ('account_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.incomecategory', verbose_name='カテゴリ')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='money.incomeitem', verbose_name='支出項目')),
                ('user_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='money.incomeorigitem', verbose_name='支出項目')),
            ],
        ),
    ]