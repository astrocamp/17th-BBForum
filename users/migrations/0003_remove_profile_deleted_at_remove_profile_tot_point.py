# Generated by Django 5.1 on 2024-08-28 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_deleted_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='tot_point',
        ),
    ]
