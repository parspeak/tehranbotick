# Generated by Django 5.1.3 on 2024-12-08 14:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-id'], 'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
        migrations.AlterField(
            model_name='image',
            name='alt_text',
            field=models.CharField(max_length=255, verbose_name='Alternative Text'),
        ),
        migrations.AlterField(
            model_name='image',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='image',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='image',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Modified'),
        ),
        migrations.AlterField(
            model_name='image',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Last Modified By'),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
    ]
