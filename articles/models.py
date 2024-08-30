from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from lib.models.soft_delete import SoftDeleteable, SoftDeleteManager
# Create your models here.
class Article(SoftDeleteable, models.Model):
    title = models.CharField(max_length=200)
    stockID=models.CharField(max_length=10)
    content = models.TextField()
    post_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    photo=models.ImageField(upload_to='images/', null=True, blank=True)
    deleted_at=models.DateTimeField(default=None, null=True,blank=True)
    userID = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
    objects = SoftDeleteManager()

#upload_to='images/'：這個參數指定圖片上傳後存放的文件夾路徑。文件將存儲在 MEDIA_ROOT/images/ 目錄下。MEDIA_ROOT 是你在 Django 設置中配置的媒體文件根目錄。
#null=True, blank=True：允許該欄位為空。
    

    class Meta:
        indexes = [models.Index(fields=["deleted_at"])] 
        #用於指定模型的索引。索引可以提高查詢效率，尤其是對於大型數據集的查詢。
        #軟刪除邏輯：通常，軟刪除功能會在 deleted_at 字段上進行頻繁的查詢操作，通過索引可以有效減少查詢的時間成本