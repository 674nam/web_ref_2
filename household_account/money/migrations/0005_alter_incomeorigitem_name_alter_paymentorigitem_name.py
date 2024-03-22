# Generated by Django 4.2.2 on 2024-03-21 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0004_alter_budget_options_alter_income_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomeorigitem',
            name='name',
            field=models.CharField(max_length=32, verbose_name='ユーザー設定収入項目'),
        ),
        migrations.AlterField(
            model_name='paymentorigitem',
            name='name',
            field=models.CharField(max_length=32, verbose_name='ユーザー設定支出項目'),
        ),
    ]