# Generated by Django 5.1.1 on 2024-09-16 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_article_deleted_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='created_at',
        ),
    ]
