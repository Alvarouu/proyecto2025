# Generated by Django 5.1.7 on 2025-06-09 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_franjahoraria_horafin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ausencia',
            name='horario',
        ),
    ]
