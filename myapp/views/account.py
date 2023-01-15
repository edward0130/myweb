from django import forms
from django.shortcuts import render, redirect

from myapp import models
from myapp.utils import bootstrap
from myapp.utils.encrypt import md5


class LoginForm(bootstrap.BootStrapForm):
    username = forms.CharField(label="用户名",
                               widget=forms.TextInput(attrs={"class": "form-control"}, ),
                               required=True
                               )
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={"class": "form-control"}, render_value=True),
                               required=True
                               )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        form.cleaned_data
        row = models.Admin.objects.filter(**form.cleaned_data).first()
        if row:
            request.session["info"] = {"id": row.id, "name": row.username}
            return redirect("/depart/list/")
        else:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})
    return render(request, "login.html", {"form": form})
