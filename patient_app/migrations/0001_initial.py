# Generated by Django 5.0 on 2023-12-14 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('last_updated', models.DateTimeField()),
            ],
        ),
    ]
