# Generated by Django 3.2.5 on 2022-02-18 16:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('link_shortener_app', '0011_alter_linkreferences_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkreferences',
            name='creation_date',
            field=models.DateField(default=datetime.datetime(2022, 2, 18, 16, 6, 5, 600798, tzinfo=utc)),
        ),
    ]
