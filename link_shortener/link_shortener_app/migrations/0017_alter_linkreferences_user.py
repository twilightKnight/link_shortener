# Generated by Django 3.2.5 on 2022-02-18 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('link_shortener_app', '0016_alter_linkreferences_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkreferences',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='link_shortener_app.userdata'),
        ),
    ]
