# Generated by Django 5.1.1 on 2024-09-14 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0013_remove_article_deleted_at_article_points_awarded"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="deleted_at",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
