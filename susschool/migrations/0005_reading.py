# Generated by Django 2.2.9 on 2020-02-02 20:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('susschool', '0004_delete_reading'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='susschool.Area')),
            ],
        ),
    ]
