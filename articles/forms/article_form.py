from django.forms import ModelForm
from django.forms.widgets import Textarea, TextInput,ClearableFileInput

from articles.models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "stockID", "content", "photo"]
        labels = {"title": "標題", 
                  "stockID":"tag公司名稱",
                  "content" :"內文",
                  "photo":"附圖片",
                  
                  }
        widgets = {
            "title": TextInput(attrs={'class': 'form-control'}),
            "stockID": TextInput(attrs={'class': 'form-control'}),
            "content": Textarea(attrs={'class': 'form-control', 'rows':8 , 'cols': 80}),
            "photo": ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
