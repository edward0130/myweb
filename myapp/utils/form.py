from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from myapp.utils.bootstrap import BootStrapModelForm
from myapp import models
from myapp.utils import encrypt


# ModelForm--User
class UserModelForm(BootStrapModelForm):
    # 通过这种方式增加样式
    # name = forms.CharField(min_length=3, label="用户", widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = models.UserInfo
        fields = '__all__'

        # 通过这种方式增加样式
        # widgets = {
        #    "name": forms.TextInput(attrs={"class": "form-control"}),
        #    "password": forms.TextInput(attrs={"class": "form-control"}),
        # }


class PrettyModelForm(BootStrapModelForm):
    # 输入内容校验 方式一
    # mobile = forms.CharField(
    #    label="电话号码",
    #   validators=[RegexValidator(r'^1[3-9]\d{9}$', "请输入有效手机号码"), ]
    #    # validators=[RegexValidator(r'^\d{11}$', "请输入有效手机号码"), ]
    # )

    class Meta:
        model = models.PrettyNum
        # fields = ["id", "mobile", "price"]
        fields = "__all__"

    # 输入内容校验 方式二
    def clean_mobile(self):
        mobile_txt = self.cleaned_data["mobile"]

        if models.PrettyNum.objects.filter(mobile=mobile_txt).exists():
            raise ValidationError("电话号码不能重复")

        if len(mobile_txt) != 11:
            raise ValidationError("格式错误")

        return mobile_txt


class PrettyEditModelForm(BootStrapModelForm):
    # 输入内容校验 方式一
    # mobile = forms.CharField(
    #    label="电话号码",
    #   validators=[RegexValidator(r'^1[3-9]\d{9}$', "请输入有效手机号码"), ]
    #    # validators=[RegexValidator(r'^\d{11}$', "请输入有效手机号码"), ]
    # )

    # 设置字段不可修改
    # mobile = forms.CharField(disabled=True, label="手机号码")

    class Meta:
        model = models.PrettyNum
        # fields = ["id", "mobile", "price"]
        fields = "__all__"

    # 输入内容校验 方式二
    def clean_mobile(self):
        mobile_txt = self.cleaned_data["mobile"]

        # print(self.instance.pk)
        # print(self.instance.id)
        # 排除 id为被修改数据 exclude(id=self.instance.pk)
        if models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=mobile_txt).exists():
            raise ValidationError("电话号码不能重复")

        if len(mobile_txt) != 11:
            raise ValidationError("格式错误")

        return mobile_txt


class AdminModelForm(BootStrapModelForm):
    confirm = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return encrypt.md5(password)

    def clean_confirm(self):
        confirm = encrypt.md5(self.cleaned_data.get("confirm"))
        password = self.cleaned_data.get("password")

        if password != confirm:
            raise ValidationError("密码不一致")
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootStrapModelForm):
    confirm = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = encrypt.md5(self.cleaned_data.get("password"))

        exists = models.Admin.objects.filter(id=self.instance.pk, password=password).exists()
        if exists:
            raise ValidationError("密码不能与历史密码重复")
        return password

    def clean_confirm(self):
        confirm = encrypt.md5(self.cleaned_data.get("confirm"))
        password = self.cleaned_data.get("password")

        if password != confirm:
            raise ValidationError("密码不一致")
        return confirm


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ['oid', 'admin']


