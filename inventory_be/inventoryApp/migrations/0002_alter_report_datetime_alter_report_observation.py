# Generated by Django 4.0.2 on 2022-06-30 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='dateTime',
            field=models.DateTimeField(default=datetime.date(2022, 6, 30)),
        ),
        migrations.AlterField(
            model_name='report',
            name='observation',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
