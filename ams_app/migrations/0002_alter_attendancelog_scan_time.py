# Generated by Django 4.1.7 on 2023-04-07 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancelog',
            name='scan_time',
            field=models.TimeField(),
        ),
    ]
