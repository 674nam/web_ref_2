# Generated by Django 4.2.2 on 2024-03-25 06:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0006_alter_incomeorigitem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='budget_limit',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='月予算'),
        ),
        migrations.AlterField(
            model_name='budget',
            name='month',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(12)], verbose_name='月'),
        ),
        migrations.AlterField(
            model_name='budget',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='年'),
        ),
        migrations.AlterField(
            model_name='income',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='金額'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='金額'),
        ),
    ]