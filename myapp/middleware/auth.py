from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import HttpResponse, render, redirect


class AuthMiddleware(MiddlewareMixin):
    """

    """

    def process_request(self, request):

        # 方法没有返回值 默认为none, 继续向后
        # 设置返回值 HttpResponse, render, redirect

        # 获取请求 url 路径信息， 判断如果是登录页面直接跳过session验证
        if request.path_info in ["/login/", "/image/code/", "/admin/add/"]:
            return

        # 获取session信息
        info_dict = request.session.get("info")
        if info_dict:
            return

        return redirect("/login/")

        # print("auth check")
        # return HttpResponse("验证失败")

    def process_response(self, request, response):

        # print("auth response")
        return response
