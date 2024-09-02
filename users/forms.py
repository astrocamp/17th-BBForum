# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError("密碼長度必須至少為8個字符。")
        if password1.isdigit():
            raise ValidationError("密碼不能僅包含數字。")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        if password2 != self.cleaned_data.get("password1"):
            raise ValidationError("兩次輸入的密碼不一致。")
        return password2
