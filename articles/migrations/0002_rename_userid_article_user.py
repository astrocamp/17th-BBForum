# Generated by Django 5.1 on 2024-09-05 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="userID",
            new_name="user",
        ),
    ]
