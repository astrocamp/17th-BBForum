from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"


def ready(self):
    from django.contrib.auth.models import Group, User
    from django.db.models.signals import post_save

    # 在資料庫遷移後創建組
    post_migrate.connect(create_groups, sender=self)

    # 為新創建的使用者設定預設群組
    post_save.connect(assign_default_group, sender=User)


def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group

    for i in range(50):
        group_name = f"LV.{i}"
        Group.objects.get_or_create(name=group_name)


def assign_default_group(sender, instance, created, **kwargs):
    from django.contrib.auth.models import Group

    if created:  # 確保只對新創建的使用者進行操作
        default_group, created = Group.objects.get_or_create(name="LV.0")
        instance.groups.add(default_group)
