# Generated by Django 4.1.7 on 2023-04-09 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ams_app', '0004_alter_attendancelog_scan_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='profile_pic',
        ),
    ]
