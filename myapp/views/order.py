from datetime import datetime
import random

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from myapp import models
from myapp.utils.form import OrderModelForm
from myapp.utils.pagination import Pagination


def order_list(request):
    queryset = models.Order.objects.all().order_by("-id")
    form = OrderModelForm()

    # 引入类，传参
    page_object = Pagination(request, queryset)
    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 获取分页展示的数据内容
        "page_str": page_object.html()}  # 展示分页页面内容

    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    """ Ajax 请求"""

    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 系统生成订单ID
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # 从session中获取管理员信息
        form.instance.admin_id = request.session["info"]["id"]

        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_del(request):
    uid = request.GET.get("uid")

    exists = models.Order.objects.filter(id=uid).exists()
    if exists:
        models.Order.objects.filter(id=uid).delete()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "errors": "没有订单数据"})


def order_detail(request):
    uid = request.GET.get("uid")

    exists = models.Order.objects.filter(id=uid).exists()
    if exists:
        row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()

        result = {
            "status": True,
            "data": row_dict
        }
        return JsonResponse(result)

    return JsonResponse({"status": False, "errors": "没有订单数据"})


def order_edit(request):
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "没有订单数据"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
