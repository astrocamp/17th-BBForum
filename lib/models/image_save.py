from django.db import models


class ImageSaveMixin:
    def save(self, *args, **kwargs):
        if self.pk:  # 檢查是否為更新操作
            try:
                old_instance = self.__class__.objects.get(pk=self.pk)
                if old_instance.photo and old_instance.photo != self.photo:
                    print(f"Deleting old photo: {old_instance.photo}")  # 調試信息
                    old_instance.photo.delete(save=False)  # 刪除舊的圖片文件
                else:
                    print(
                        "No old photo to delete or no change in photo."
                    )  # 如果圖片沒變或沒有舊圖片
            except self.__class__.DoesNotExist:
                print("Old instance does not exist.")  # 如果舊的實例不存在
        super().save(*args, **kwargs)
