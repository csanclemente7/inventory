# Generated by Django 4.0.2 on 2022-07-04 23:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryApp', '0008_alter_report_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 4, 23, 59, 51, 653093, tzinfo=utc)),
        ),
    ]
