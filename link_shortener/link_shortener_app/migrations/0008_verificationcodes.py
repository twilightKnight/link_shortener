# Generated by Django 3.2.5 on 2021-09-27 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_shortener_app', '0007_userdata_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=50)),
            ],
        ),
    ]
