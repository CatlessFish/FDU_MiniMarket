from datetime import date
from django import forms
from django.forms import fields
from django.contrib.auth.forms import(
    ReadOnlyPasswordHashField, AuthenticationForm
)
from django.core.exceptions import ValidationError

from .models import SiteUser

class UserCreationForm_super(forms.ModelForm):
    """
    A form for creating new users
    !!! Designed for SUPERUSER ONLY !!!
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm your password", widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('username', 'nickname', 'building_no', 'room_no', 'contact', 'is_staff', )
        help_texts = {
            'username': '用于登录的用户名',
            'nickname': '用于展示的昵称',
            'building_no': '楼号',
            'room_no': '房间号',
        }
        error_messages = {
            'username': { # 错误提示信息
                'max_length': "Username too long", # 对应表单字段上的限制
                'unique': '用户名已被占用！',
            },
            'nickname': {
                'unique': "昵称已被占用！",
            }
        }


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match!")
        return password2

    def save(self, commit=True): # 重写save方法
        user = super().save(commit=False) # 调用超类的save方法得到user，但是不commit
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserCreationForm(UserCreationForm_super):
    """
    A form for new users registration
    """
    class Meta:
        model = SiteUser
        fields = ('username', 'nickname', 'building_no', 'room_no', 'contact')


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SiteUser
        fields = ('nickname', 'building_no', 'room_no', 'contact',)
        

class LoginForm(forms.Form):
    username = fields.CharField(
        label='Username',
        required=True,
        max_length=18,
        error_messages={
            "required":"用户名不可以为空",
            "max_length":"用户名不能超过18位"
        }
    )
    password = fields.CharField(
        label='Password',
        required=True,
        widget=forms.widgets.PasswordInput(),
        error_messages={
            "required":"密码不可以空",
        }
    )