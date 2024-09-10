from django import forms
from django.forms import ModelForm
from taggit.forms import TagField

from articles.models import Article


class ArticleForm(ModelForm):
    tags = TagField()

    class Meta:
        model = Article
        fields = ["title", "tags", "content", "photo"]
        labels = {
            "title": "Title",
            "tags": "Tags",
            "content": "Content",
            "photo": "Photo",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "tags": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 8, "cols": 80}
            ),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get("photo"):
            instance.photo = self.cleaned_data["photo"]
        if commit:
            instance.save()
        return instance
