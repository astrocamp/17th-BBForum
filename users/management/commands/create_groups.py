from django.core.management.base import BaseCommand

from users.apps import UsersConfig, create_groups


class Command(BaseCommand):
    help = "手動創建 LV0-49 群組"

    def handle(self, *args, **kwargs):
        self.stdout.write("手動創建群組...")
        create_groups(UsersConfig)
        self.stdout.write(self.style.SUCCESS("群組創建完成"))
