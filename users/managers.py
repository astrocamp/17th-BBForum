from django.db import models


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)
