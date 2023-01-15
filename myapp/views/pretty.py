from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from myapp import models

from myapp.utils.form import PrettyModelForm, PrettyEditModelForm

from myapp.utils.pagination import Pagination


def pretty_list(request):
    """" 靓号列表 """

    # # 查询过滤 <QuerySet [<PrettyNum: PrettyNum object (1)>]>
    # q = models.PrettyNum.objects.filter(id=1, mobile="12333333333")
    # print(q)
    # filter_dict = {"id": 1, "mobile": "12333333333"}
    # q1 = models.PrettyNum.objects.filter(**filter_dict)
    # print(q1)
    #
    # # 查询条件
    # q2 = models.PrettyNum.objects.filter(id__gt=1)  # id > 1  :id__gte, id__lte
    # print(q2)
    # q3 = models.PrettyNum.objects.filter(mobile__contains="")

    # 数据搜索
    filter_dict = {}
    search_info = request.GET.get("query", "")
    if search_info:
        filter_dict["mobile__contains"] = search_info

    data_list = models.PrettyNum.objects.filter(**filter_dict)

    page_object = Pagination(request, data_list)
    context = {
        "data_list": page_object.page_queryset,
        "search_info": search_info,
        "page_str": page_object.html()}

    return render(request, "pretty_list.html", context)


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    form = PrettyModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")

    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    row = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row)

        return render(request, "pretty_edit.html", {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row)

    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})


def pretty_del(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()

    return redirect("/pretty/list/")
