from django.shortcuts import render, redirect
from myapp import models

from myapp.utils.form import UserModelForm
from myapp.utils.pagination import Pagination


def user_list(request):
    """" 员工列表 """

    data_list = models.UserInfo.objects.all()

    page_object = Pagination(request, data_list)
    context = {
        "data_list": page_object.page_queryset,  # 获取分页展示的数据内容
        "page_str": page_object.html()}  # 展示分页页面内容

    return render(request, "user_list.html", context)


def user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_add.html", {"form": form})

    form = UserModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    # 校验失败
    return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    """" 修改用户信息 """

    row = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row)
        return render(request, "user_edit.html", {"form": form})

    form = UserModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    return render(request, "user_edit.html", {"form": form})


def user_del(request, nid):
    """" 删除用户 """

    # nid = request.GET.get("nid")

    r = models.UserInfo.objects.filter(id=nid).delete()

    return redirect("/user/list/")
