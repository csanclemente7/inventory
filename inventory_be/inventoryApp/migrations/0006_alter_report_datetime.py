# Generated by Django 4.0.2 on 2022-07-04 23:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryApp', '0005_alter_report_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 4, 23, 46, 7, 891737, tzinfo=utc)),
        ),
    ]
