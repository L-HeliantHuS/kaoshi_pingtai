from django.db import models

# Create your models here.

class Select(models.Model):


    id = models.IntegerField(primary_key=True, verbose_name="题号")
    topic = models.TextField(verbose_name="题目")
    a = models.CharField(max_length=255, name="a", verbose_name="A选项")
    b = models.CharField(max_length=255, name="b", verbose_name="B选项")
    c = models.CharField(max_length=255, name="c", verbose_name="C选项")
    d = models.CharField(max_length=255, name="d", verbose_name="D选项")
    key = models.CharField(max_length=1, verbose_name="答案")


class Selects(models.Model):


    id = models.IntegerField(primary_key=True, verbose_name="题号")
    topic = models.TextField(verbose_name="题目")
    a = models.CharField(max_length=255, name="a", verbose_name="A选项")
    b = models.CharField(max_length=255, name="b", verbose_name="B选项")
    c = models.CharField(max_length=255, name="c", verbose_name="C选项")
    d = models.CharField(max_length=255, name="d", verbose_name="D选项")
    key = models.CharField(max_length=4, verbose_name="答案")


class Judge(models.Model):


    id = models.IntegerField(primary_key=True, verbose_name="题号")
    topic = models.TextField(verbose_name="题目")
    key = models.BooleanField(verbose_name="答案")
