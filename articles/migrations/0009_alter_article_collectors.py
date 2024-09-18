# Generated by Django 5.1.1 on 2024-09-17 03:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0008_remove_comment_collectors"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="collectors",
            field=models.ManyToManyField(
                blank=True, related_name="collectors", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
