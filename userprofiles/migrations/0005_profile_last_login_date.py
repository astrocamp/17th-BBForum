# Generated by Django 5.1.1 on 2024-09-13 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userprofiles", "0004_alter_profile_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="last_login_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
