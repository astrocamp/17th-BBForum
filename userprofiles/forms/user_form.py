from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import DateInput, EmailInput, PasswordInput, TextInput
from django.utils import timezone

from userprofiles.choice import (
    Education_level,
    Gender,
    Inves_attributes,
    Investment_experience_choices,
    Investment_tools,
    Profession,
    Taiwan_regions,
)
from userprofiles.models import Profile


class ProfileForm(ModelForm):

    gender = forms.TypedChoiceField(
        choices=Gender.choices,
        required=False,
        label="性    別:",
        widget=forms.RadioSelect(),
    )

    location = forms.ChoiceField(
        choices=Taiwan_regions,
        required=True,
        label="居住地區:",
        widget=forms.Select(
            attrs={
                "class": " rounded-l  bg-gray-94 pl-2.5 pr-2.5 border border--gray-300 shadow-area "
            }
        ),
    )

    education = forms.ChoiceField(
        choices=Education_level.choices,
        required=True,
        label="教育程度:",
        widget=forms.Select(
            attrs={
                "class": " rounded-l bg-gray-94 shadow-area pl-2.5 pr-2.5 border border-gray-300 focus:border-red-primary focus:outline-none focus:ring-0"
            }
        ),
    )

    profession = forms.ChoiceField(
        choices=Profession,
        required=True,
        label="職    業:",
        widget=forms.Select(
            attrs={
                "class": "  rounded-l bg-gray-94 shadow-area pl-2.5 pr-2.5 border border-gray-300 focus:border-red-primary focus:outline-none focus:ring-0"
            }
        ),
    )

    investment_experience = forms.ChoiceField(
        choices=Investment_experience_choices,
        required=True,
        label="投資經驗:",
        widget=forms.Select(
            attrs={
                "class": " rounded-l bg-gray-94  shadow-area pl-2.5 pr-2.5 border border-gray-300 focus:border-red-primary focus:outline-none focus:ring-0"
            }
        ),
    )

    investment_tool = forms.MultipleChoiceField(
        choices=Investment_tools,
        required=True,
        label="投資工具:",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "flex"}),
    )

    investment_attributes = forms.TypedChoiceField(
        choices=Inves_attributes.choices,
        required=True,
        label="投資屬性:",
        widget=forms.Select(
            attrs={
                "class": "  rounded-l bg-gray-94  shadow-area pl-2.5 pr-2.5 border border-gray-300 focus:border-red-primary focus:outline-none focus:ring-0"
            }
        ),
    )

    class Meta:
        model = Profile
        fields = [
            "nickname",
            "user_img",
            "gender",
            "birthday",
            "location",
            "education",
            "profession",
            "investment_experience",
            "investment_tool",
            "investment_attributes",
        ]
        labels = {
            "nickname": "暱稱",
            "user_img": "會員頭像",
            "gender": "性別",
            "birthday": "生日",
            "location": "居住地區",
            "education": "教育程度",
            "profession": "職業",
            "investment_experience": "投資經驗",
            "investment_tool": "投資工具",
            "investment_attributes": "投資屬性",
        }

        widgets = {
            "nickname": TextInput(
                attrs={
                    "class": " rounded-l bg-gray-94  shadow-area pl-2.5 pr-2.5 border border-gray-300 focus:border-red-primary focus:outline-none focus:ring-0",
                }
            ),
            "birthday": DateInput(
                attrs={
                    "type": "date",
                    "class": " rounded-l bg-gray-94  shadow-area pl-2.5 pr-2.5 border border-gray-300 focus:border-red-primary focus:outline-none focus:ring-0",
                }
            ),
            "user_img": forms.FileInput(attrs={"class": "form-control-file"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def clean_investment_tool(self):
        data = self.cleaned_data.get("investment_tool")
        if not data:
            raise ValidationError("請選擇至少一個投資工具。")
        return data

    def clean_user_img(self):
        user_img = self.cleaned_data.get("user_img")
        if not user_img:
            raise ValidationError("請上傳您的圖片。")
        return user_img

    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if birthday and birthday > timezone.now().date():
            raise forms.ValidationError("生日不能選擇未來的日期。")
        return birthday


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
