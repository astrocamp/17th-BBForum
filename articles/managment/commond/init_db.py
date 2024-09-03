from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Initialize default groups'

    def handle(self, *args, **kwargs):
        Group.objects.get_or_create(name='Default Group')
        self.stdout.write(self.style.SUCCESS('Successfully initialized groups'))