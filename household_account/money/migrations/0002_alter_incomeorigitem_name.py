# Generated by Django 4.2.2 on 2024-03-17 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomeorigitem',
            name='name',
            field=models.CharField(max_length=32, verbose_name='ユーザー設定収入項目'),
        ),
    ]
