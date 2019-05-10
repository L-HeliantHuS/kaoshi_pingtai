from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Select(models.Model):


    id = models.IntegerField(primary_key=True, verbose_name="题号")
    topic = models.TextField(verbose_name="题目")
    a = models.CharField(max_length=255, name="a", verbose_name="A选项")
    b = models.CharField(max_length=255, name="b", verbose_name="B选项")
    c = models.CharField(max_length=255, name="c", verbose_name="C选项")
    d = models.CharField(max_length=255, name="d", verbose_name="D选项")
    key = models.CharField(max_length=1, verbose_name="答案")

    class Meta:
        verbose_name_plural = "单选题"


class Selects(models.Model):


    id = models.IntegerField(primary_key=True, verbose_name="题号")
    topic = models.TextField(verbose_name="题目")
    a = models.CharField(max_length=255, name="a", verbose_name="A选项")
    b = models.CharField(max_length=255, name="b", verbose_name="B选项")
    c = models.CharField(max_length=255, name="c", verbose_name="C选项")
    d = models.CharField(max_length=255, name="d", verbose_name="D选项")
    key = models.CharField(max_length=4, verbose_name="答案")

    class Meta:
        verbose_name_plural = "多选题"


class Judge(models.Model):


    id = models.IntegerField(primary_key=True, verbose_name="题号")
    topic = models.TextField(verbose_name="题目")
    key = models.BooleanField(verbose_name="答案")

    class Meta:
        verbose_name_plural = "判断题"


class Bugs(models.Model):


    id = models.IntegerField(auto_created=True, primary_key=True, verbose_name="序号", unique=True)
    title = models.CharField(max_length=255, verbose_name="标题")
    date = models.DateTimeField(auto_now_add=True, verbose_name="日期")
    content = models.TextField(verbose_name="内容")

    class Meta:
        verbose_name_plural = "更新日志"


class UserInfo(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fraction = models.BigIntegerField(default=0, auto_created=True)  # 做题时间
    total = models.BigIntegerField(default=0, auto_created=True)  # 做题总数
    ttotal = models.BigIntegerField(default=0, auto_created=True)  # 对题总数
    ftotal = models.BigIntegerField(default=0, auto_created=True)  # 错题总数

    class Meta:
        verbose_name_plural = "用户其他信息"
