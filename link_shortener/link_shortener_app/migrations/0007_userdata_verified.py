# Generated by Django 3.2.5 on 2021-09-27 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_shortener_app', '0006_rename_registrationform_userdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]