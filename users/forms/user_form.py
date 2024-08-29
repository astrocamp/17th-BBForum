
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput,EmailInput,PasswordInput,DateInput
from users.models import Profile
from django.contrib.auth.models import User
from users.choice import TAIWAN_REGIONS,Gender,EducationLevel,Inves_attributes,INVESTMENT_TOOLS,INVESTMENT_EXPERIENCE_CHOICES


class ProfileForm(ModelForm):
    gender = forms.TypedChoiceField(
        choices=Gender.choices,
        required=False,
        widget=forms.Select
    )

    location = forms.ChoiceField(choices=TAIWAN_REGIONS, required=True)

    education = forms.ChoiceField(
        choices=EducationLevel.choices,
        required=True,
        widget=forms.Select
    )

    investment_experience = forms.ChoiceField(
        choices=INVESTMENT_EXPERIENCE_CHOICES,
        required=True,  # 設置為必填
        widget=forms.Select,
    )

    investment_tool = forms.MultipleChoiceField(
        choices=INVESTMENT_TOOLS,
        required=True,  # 如果不需要必填，可以設為 False
        widget=forms.CheckboxSelectMultiple,
    )

    investment_attributes = forms.TypedChoiceField(
        choices=Inves_attributes.choices,
        required=True ,
        widget=forms.Select,
    )
    
    class Meta:
        model = Profile
        fields = [
            "nickname", "gender", "birthday", "location", "education",
            "Investment_experience", "Investment_tool", "investment_attributes",

        ]
        labels = {
            "nickname": "暱稱",
            "gender": "性別",
            "birthday": "生日",
            "location": "居住地區",
            "education": "教育程度",
            "Investment_experience": "投資經驗",
            "Investment_tool": "投資工具",
            "investment_attributes": "投資屬性",

        }
        widgets = {
            "nickname": TextInput(),
            "birthday":DateInput(attrs={'type': 'date'}),
            # "location": forms.Select(),
            # "education": forms.Select(),
            # "Investment_experience": forms.Select(), 
            # "Investment_tool": forms.SelectMultiple(),

      
        }

  

class UserForm(ModelForm):
    class Meta:
        model:User
        fields = ["username", "password", "email"]
        labels = {
        "username":"真實姓名",
        "password":"密碼",
        "email":"電子信箱",
        }
        widgets = {
        "username":TextInput(),
        "password":PasswordInput,
        "email":EmailInput(),            
        }
