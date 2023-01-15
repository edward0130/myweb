"""
    自定义分页组件

    使用说明：
    def pretty_list(request):

        queryset= models.PrettyNum.objects.all()

        #引入类，传参
        page_object = Pagination(request, queryset)
        context = {
            "queryset": page_object.page_queryset, #获取分页展示的数据内容
            "page_str": page_object.html()}        #展示分页页面内容

        return render(request, "pretty_list.html", context)

    html页面添加内容

        <nav aria-label="...">
            <ul class="pagination">
                {{ page_str }}
            </ul>
        </nav>

"""
import copy

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, param="page", plus=4):

        # 拷贝请求参数字典，对字典数据使用setlist()方法进行更新，使用urlencode()方法进行拼接
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page_str = request.GET.get("page", "1")
        if page_str.isdecimal():
            page = int(page_str)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.plus = plus
        self.param = param

        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 展示数据
        self.page_queryset = queryset[self.start:self.end]

        # 获取数据总数
        total_count = queryset.count()
        page_total_size, div = divmod(total_count, page_size)
        if div:
            page_total_size += 1

        self.page_total_size = page_total_size

    def html(self):
        # 分页页码
        self.plus = 5
        # 总页码 小于 一次展示分页数量
        if self.page_total_size <= self.plus * 2 + 1:
            start_page = 1
            end_page = self.page_total_size
        else:
            # 当前页 小于 左侧可展示的数量
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页 大于 右侧可展示的数量
                if self.page > self.page_total_size - self.plus:
                    start_page = self.page_total_size - 2 * self.plus
                    end_page = self.page_total_size
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 分页展示
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.param, [1])
        ele = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.param, [self.page - 1])
            ele = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.param, [1])
            ele = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)

        # 中间页码
        for i in range(start_page, end_page + 1):
            if i == self.page:
                self.query_dict.setlist(self.param, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.param, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.page_total_size:
            self.query_dict.setlist(self.param, [self.page + 1])
            ele = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.param, [self.page_total_size])
            ele = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)

        # 尾页
        self.query_dict.setlist(self.param, [self.page_total_size])
        ele = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(ele)

        # 跳转
        page_jump_str = """
                        <li>
                            <form method="get" style="float: right; width: 115px">
                                <div class="input-group">
                                    <input type="text"  name="page" class="form-control" placeholder="页码">
                                    <span class="input-group-btn">
                                    <button class="btn btn-default" type="submit">跳转</button>
                                </span>
                                </div>
                            </form>
                        </li>
            """
        page_str_list.append(page_jump_str)
        page_str = mark_safe("".join(page_str_list))
        return page_str
