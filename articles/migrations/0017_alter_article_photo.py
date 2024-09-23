# Generated by Django 5.1.1 on 2024-09-23 07:57

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0016_article_collectors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=storages.backends.s3.S3Storage,
                upload_to="images/",
            ),
        ),
    ]
