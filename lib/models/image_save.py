import io

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image


class ImageSaveMixin:
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = self.__class__.objects.get(pk=self.pk)
                if old_instance.photo and old_instance.photo != self.photo:
                    print(f"Deleting old photo: {old_instance.photo}")
                    old_instance.photo.delete(save=False)
                else:
                    print("No old photo to delete or no change in photo.")
            except self.__class__.DoesNotExist:
                print("Old instance does not exist.")

        # 在保存之前檢查圖片大小
        if self.photo:
            print("重新壓縮照片檔案")
            img = Image.open(self.photo)
            img_size = self.photo.size
            if img_size > 500 * 1024:
                img_io = io.BytesIO()
                img.save(img_io, format="WEBP", quality=80)
                img_io.seek(0)
                self.photo.save(self.photo.name, ContentFile(img_io.read()), save=False)

        super().save(*args, **kwargs)
