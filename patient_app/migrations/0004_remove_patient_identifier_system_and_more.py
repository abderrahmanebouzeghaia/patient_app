# Generated by Django 5.0 on 2023-12-16 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0003_remove_patient_last_updated_remove_patient_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='identifier_system',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='identifier_value',
        ),
    ]
