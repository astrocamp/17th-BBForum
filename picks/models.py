from django.db import models
from django.contrib.auth.models import User
from articles.models import IndustryTag

class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(IndustryTag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'stock') 

User.add_to_class('stocks', models.ManyToManyField(IndustryTag, through=UserStock, blank=True))
