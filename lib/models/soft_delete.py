from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class SoftDeleteable:
    def delete(self):  # Article.delete() 假裝刪除
        self.deleted_at = timezone.now()
        self.save()

    def really_delete(self):  # 真刪除
        self.delete()

    objects = SoftDeleteManager()  # articles.models Article己設定