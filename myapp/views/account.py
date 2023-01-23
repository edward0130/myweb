from io import BytesIO

from django import forms
from django.shortcuts import render, redirect, HttpResponse

from myapp import models
from myapp.utils import bootstrap, checkcode
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
    code = forms.CharField(label="验证码",
                           widget=forms.TextInput(attrs={"class": "form-control"}, ),
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

        # 获取输入验证码信息， 同时把记录到session的code信息删除掉，便于从数据查询数据
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")

        # 对验证码信息进行校验
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})

        row = models.Admin.objects.filter(**form.cleaned_data).first()
        if row:
            request.session["info"] = {"id": row.id, "name": row.username}
            # 验证成功，重新设置session过期时间
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect("/depart/list/")
        else:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})
    return render(request, "login.html", {"form": form})


def image_code(request):

    # 获取随机生成验证码
    img, code_str = checkcode.check_code()

    # 记录session信息
    request.session["image_code"] = code_str
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, "png")

    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.clear()

    return redirect("/login/")
