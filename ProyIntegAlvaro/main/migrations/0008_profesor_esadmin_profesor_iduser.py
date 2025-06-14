# Generated by Django 5.1.7 on 2025-04-17 09:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_profesor_contrasenia_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profesor',
            name='esAdmin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profesor',
            name='idUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
