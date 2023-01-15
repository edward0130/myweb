from django.shortcuts import render, redirect
from myapp import models


def depart_list(request):
    """部门列表"""

    # 从数据库获取数据
    # 查询集合  [数据对象],[数据对象],[数据对象]
    data_list = models.Department.objects.all()

    return render(request, "depart_list.html", {"data_list": data_list})


def depart_add(request):
    """ 添加部门 """

    # 显示添加部门页面
    if request.method == "GET":
        return render(request, "depart_add.html")

    # 获取表单中的数据
    title = request.POST.get("title")

    # 插入到数据库中
    models.Department.objects.create(title=title)

    return redirect("/depart/list")


def depart_delete(request):
    """ 删除部门 """

    # 获取部门ID
    nid = request.GET.get("nid")

    # 删除库内数据
    models.Department.objects.filter(id=nid).delete()

    return redirect("/depart/list")


def depart_edit(request, nid):
    """ 编写部门信息 """

    if request.method == "GET":
        data = models.Department.objects.filter(id=nid).first()

        return render(request, "depart_edit.html", {"data": data})

    title = request.POST.get("title")

    models.Department.objects.filter(id=nid).update(title=title)

    return redirect("/depart/list")
