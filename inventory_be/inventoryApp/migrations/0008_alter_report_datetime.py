# Generated by Django 4.0.2 on 2022-07-04 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryApp', '0007_alter_report_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='dateTime',
            field=models.DateTimeField(),
        ),
    ]
