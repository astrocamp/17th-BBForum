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
        super().save(*args, **kwargs)
