from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'

    def ready(self):
        # 將 Group 的導入放在 ready 方法內部
        from django.contrib.auth.models import Group
        # 在資料庫遷移後創建組
        post_migrate.connect(create_groups, sender=self)

def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    for i in range(50):
        group_name = f"LV.{i}"
        Group.objects.get_or_create(name=group_name)