# Generated by Django 5.1.3 on 2024-12-08 14:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Is Admin'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='One-Time Password (OTP)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp_expiry',
            field=models.DateTimeField(blank=True, null=True, verbose_name='OTP Expiry'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone', message='Enter a valid phone number.', regex='^09(0[0-5]|[1 3]\\d|2[0-3]|9[0-9]|41)\\d{7}$')], verbose_name='Phone Number'),
        ),
    ]
