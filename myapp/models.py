from django.db import models


# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")

    # 设置外键 depart+id
    # 部门表被删除  1.级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)

    # 部门表被删除  1.置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # django 转换
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class Department(models.Model):
    title = models.CharField(verbose_name="部门名称", max_length=64)

    def __str__(self):
        return self.title


class PrettyNum(models.Model):

    """ 靓号 """

    #  null=True, blank=True
    mobile = models.CharField(verbose_name="电话号码", max_length=32)

    price = models.IntegerField(verbose_name="价钱", default=0)

    level_choices = (
        (1, "一级"),
        (2, "二级")
    )
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=1)

    status_choices = (
        (1, "未占用"),
        (2, "已占用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)


class Admin(models.Model):
    """ 登录用户 """

    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)


