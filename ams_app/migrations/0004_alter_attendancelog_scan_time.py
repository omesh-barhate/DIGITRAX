# Generated by Django 4.1.7 on 2023-04-08 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams_app', '0003_alter_attendancelog_scan_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancelog',
            name='scan_time',
            field=models.TimeField(),
        ),
    ]
