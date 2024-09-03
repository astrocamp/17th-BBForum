from django.db import models

class ImageSaveMixin:
    def save(self, *args, **kwargs):
        if self.pk:  # 檢查是否為更新操作
            try:
                old_instance = self.__class__.objects.get(pk=self.pk)
                if old_instance.photo and old_instance.photo != self.photo:
                    old_instance.photo.delete(save=False)  # 刪除舊的圖片文件
            except self.__class__.DoesNotExist:
                pass
        super().save(*args, **kwargs)