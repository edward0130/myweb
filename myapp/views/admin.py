from django.shortcuts import render, redirect
from myapp import models

from myapp.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from myapp.utils.pagination import Pagination


def admin_list(request):

    queryset = models.Admin.objects.all()

    page_object = Pagination(request, queryset)
    context = {
        "data_list": page_object.page_queryset,  # 获取分页展示的数据内容
        "page_str": page_object.html()}  # 展示分页页面内容

    return render(request, "admin_list.html", context)


def admin_add(request):

    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "change.html", {"form": form, "title": title})


def admin_edit(request, nid):
    title = "编辑管理员"

    # 判断数据是否存在
    obj = models.Admin.objects.filter(id=nid).first()
    if not obj:
        return redirect("/admin/list/")

    if request.method == "GET":
        form = AdminEditModelForm(instance=obj)
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "change.html", {"form": form, "title": title})


def admin_reset(request, nid):


    obj = models.Admin.objects.filter(id=nid).first()
    if not obj:
        return redirect("/admin/list/")

    title = "重置密码 - {}".format(obj.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "change.html", {"form": form, "title": title})


def admin_del(request, nid):

    models.Admin.objects.filter(id=nid).delete()

    return redirect("/admin/list/")
