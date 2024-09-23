from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save


def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group

    for i in range(50):
        group_name = f"LV.{i}"
        Group.objects.get_or_create(name=group_name)


def assign_default_group(sender, instance, created, **kwargs):
    from django.contrib.auth.models import Group

    if created:
        default_group, created = Group.objects.get_or_create(name="LV.0")
        instance.groups.add(default_group)


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from django.contrib.auth.models import User

        post_migrate.connect(create_groups, sender=self)
        post_save.connect(assign_default_group, sender=User)
