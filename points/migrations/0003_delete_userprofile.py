# Generated by Django 5.1.1 on 2024-09-13 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("points", "0002_remove_pointsdetails_user_remove_post_user_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserProfile",
        ),
    ]
