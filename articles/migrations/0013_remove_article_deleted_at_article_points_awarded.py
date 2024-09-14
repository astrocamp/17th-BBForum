# Generated by Django 5.1.1 on 2024-09-14 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_remove_article_articles_ar_deleted_c8c4cd_idx'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='deleted_at',
        ),
        migrations.AddField(
            model_name='article',
            name='points_awarded',
            field=models.IntegerField(default=0),
        ),
    ]
