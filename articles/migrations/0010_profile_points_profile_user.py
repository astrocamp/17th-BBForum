# Generated by Django 5.1.1 on 2024-09-13 15:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0009_profile"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="points",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="article_profile",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
