# Generated by Django 5.1.7 on 2025-05-12 13:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_asignatura_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='idFranja',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.franjahoraria'),
        ),
    ]
