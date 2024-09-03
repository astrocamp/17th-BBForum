# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["username"].error_messages = {
            "required": "用戶名是必填項。",
        }

        self.fields["password1"].required = True
        self.fields["password1"].error_messages = {
            "required": "密碼是必填項。",
        }

        self.fields["password2"].required = True
        self.fields["password2"].error_messages = {
            "required": "確認密碼是必填項。",
        }

        self.fields["email"].required = True
        self.fields["email"].error_messages = {
            "required": "電子郵件地址是必填項。",
            "invalid": "請輸入有效的電子郵件地址。",
        }

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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("電子郵件地址是必填項。")
        try:
            EmailValidator()(email)
        except ValidationError:
            raise ValidationError("請輸入有效的電子郵件地址。")
        return email
