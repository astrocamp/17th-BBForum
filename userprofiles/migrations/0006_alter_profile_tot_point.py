# Generated by Django 5.1.1 on 2024-09-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0005_profile_last_login_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tot_point',
            field=models.IntegerField(default=0),
        ),
    ]
