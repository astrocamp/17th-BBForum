from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.widgets import (DateInput, EmailInput, PasswordInput,
                                  TextInput)

from users.choice import (Education_level, Gender, Inves_attributes,
                          Investment_experience_choices, Investment_tools,
                          Taiwan_regions)
from users.models import Profile


class ProfileForm(ModelForm):
    gender = forms.TypedChoiceField(
        choices=Gender.choices, required=False, label="性別", widget=forms.Select
    )

    location = forms.ChoiceField(
        choices=Taiwan_regions, required=True, label="居住地區"
    )

    education = forms.ChoiceField(
        choices=Education_level.choices,
        required=True,
        label="教育程度",
        widget=forms.Select,
    )

    investment_experience = forms.ChoiceField(
        choices=Investment_experience_choices,
        required=True,  # 設置為必填
        label="投資經驗",
        widget=forms.Select,
    )

    investment_tool = forms.MultipleChoiceField(
        choices=Investment_tools,
        required=True,  # 如果不需要必填，可以設為 False
        label="投資工具",
        widget=forms.CheckboxSelectMultiple,
    )

    investment_attributes = forms.TypedChoiceField(
        choices=Inves_attributes.choices,
        required=True,
        label="投資屬性",
        widget=forms.Select,
    )

    class Meta:
        model = Profile
        fields = [
            "nickname",
            "gender",
            "birthday",
            "location",
            "education",
            "investment_experience",
            "investment_tool",
            "investment_attributes",
        ]
        labels = {
            "nickname": "暱稱",
            "gender": "性別",
            "birthday": "生日",
            "location": "居住地區",
            "education": "教育程度",
            "investment_experience": "投資經驗",
            "investment_tool": "投資工具",
            "investment_attributes": "投資屬性",
        }
        widgets = {
            "nickname": TextInput(),
            "birthday": DateInput(attrs={"type": "date"}),
        }


class UserForm(ModelForm):
    class Meta:
        model: User
        fields = ["username", "password", "email"]
        labels = {
            "username": "真實姓名",
            "password": "密碼",
            "email": "電子信箱",
        }
        widgets = {
            "username": TextInput(),
            "password": PasswordInput,
            "email": EmailInput(),
        }
