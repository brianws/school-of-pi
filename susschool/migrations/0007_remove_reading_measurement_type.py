# Generated by Django 2.2.9 on 2020-02-03 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('susschool', '0006_reading_measurement_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reading',
            name='measurement_type',
        ),
    ]
