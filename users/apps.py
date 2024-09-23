from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from django.contrib.auth.models import Group, User
        from django.db.models.signals import post_save

        post_migrate.connect(create_groups, sender=self)
        post_save.connect(assign_default_group, sender=User)


def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group

    print("creategroups0~49")
    for i in range(50):
        group_name = f"LV.{i}"
        Group.objects.get_or_create(name=group_name)


def assign_default_group(sender, instance, created, **kwargs):
    from django.contrib.auth.models import Group

    print("creategroup LV0")
    if created:
        default_group, created = Group.objects.get_or_create(name="LV.0")
        instance.groups.add(default_group)
