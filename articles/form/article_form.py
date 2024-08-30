from django.forms import ModelForm
from django.forms.widgets import NumberInput, Textarea, TextInput

from articles.models import Article


class ArticleFormm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "price", "description"]
        labels = {"title": "title", "price": "price", "description": "description"}
        widgets = {
            "title": TextInput(),
            "price": NumberInput(),
            "description": Textarea(),
        }
