import operator
import random
import time
import os

import pandas
import psutil
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect

from kaoshi.models import Select, Selects, Judge, Bugs, UserInfo


@login_required(login_url="login")
def index(request):
    # 第一次进入会初始化一个分数.
    try:
        info = UserInfo.objects.create(user_id=request.user.id, fraction=0, total=0, ttotal=0, ftotal=0)
        info.save()
    except:
        pass
    memory = getMemorystate()

    # 获取所有题目类型的数量
    select_count = Select.objects.count()
    selects_count = Selects.objects.count()
    judge_count = Judge.objects.count()

    response = render(request, "welcome.html", {
        "memory": memory,
        "select_count": select_count,
        "selects_count": selects_count,
        "judge_count": judge_count,
        "system_select_count": settings.RANDOM_SELECT,
        "system_selects_count": settings.RANDOM_SELECTS,
        "system_judge_count": settings.RANDOM_JUDGE
    })
    return response


def login(request):
    """
    登陆
    :param request: 必备参数
    :return: render
    """
    if request.method == "GET":
        # 禁止用户登陆之后再次进入登陆页面.
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "login.html")

    elif request.method == "POST":
        username = request.POST.get("username", " ")
        password = request.POST.get("password", " ")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"error": "用户名或者密码不正确."})
    else:
        return HttpResponse("你不可以这样做。")


@login_required(login_url="login")
def logout(request):
    """
    注销
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect("/login")


def getCPUstate(interval=1):
    return (" CPU: " + str(psutil.cpu_percent(interval)) + "%")


def getMemorystate():
    phymem = psutil.virtual_memory()
    line = "Memory: %5s%% %6s/%s" % (
        phymem.percent,
        str(int(phymem.used / 1024 / 1024)) + "M",
        str(int(phymem.total / 1024 / 1024)) + "M"
    )
    return line


@login_required(login_url="login")
def select(request):
    """
    单选题
    :param request: 必要参数
    :return: render
    """
    if request.method == "GET":
        # 访问题目的时候创建一个session 保存当前的时间戳
        last = int(time.time())
        request.session["last_time"] = last
        db = Select.objects.all()
        return render(request, "select.html", {"data": db})

    elif request.method == "POST":
        keys = request.POST.getlist("select")
        if not keys:
            return HttpResponse("你倒是选择啊.")
        db = Select.objects
        true_total = 0  # 做对的题目数量
        pass_total = 0  # 做错的题目数量
        pass_key = []  # 做错的题号
        pass_value = []  # 做错的答案
        pass_index = []  # 错误索引
        keys_true = {str(i.id): i.key for i in db.all()}  # 正确答案
        temp = ""
        for i in keys:
            key, value, indexkey = i.split("|")
            if key == temp:
                return HttpResponse(f"检测到你第{indexkey}题选择了多个答案, 这次不分析成绩, 请重新开始.")
            temp = key
            if keys_true[str(key)] == value:
                true_total += 1
            else:
                pass_total += 1
                pass_value.insert(0, value)
                pass_key.append(key)
                pass_index.append(int(indexkey))  # 错误的索引

        error_topic = [db.get(id=i) for i in pass_key]
        # error_topic = db.filter(id__in=pass_key)



        pass_index.sort(reverse=True)

        print(pass_key, pass_value)

        # 提交题目, 获取当前的时间戳，并获取之前看到题目的时间戳, 进行减法运算, 得到时间.
        end_time = int(time.time())
        # 用时. 单位秒
        train_time = end_time - request.session["last_time"]

        # 修改数据库的内容
        request.user.userinfo.fraction += train_time
        request.user.userinfo.total += true_total + pass_total
        request.user.userinfo.ttotal += true_total
        request.user.userinfo.ftotal += pass_total
        request.user.userinfo.save()

        # count: 一共做了多少题目
        response = render(request, "error_pic.html", {
            "count": true_total + pass_total,
            "true_total": true_total,
            "pass_total": pass_total,
            "pass_key": pass_key,
            "error_topic": error_topic,
            "total": db.count(),
            "true_key": pass_value,
            "bfb": "%.2f" % (
                    int(true_total) / int(true_total + pass_total) * 100),
            "dual": True,
            "time": train_time,
            "pass_index": pass_index,
        })

        return response
    else:
        return HttpResponse("No")


@login_required(login_url="login")
def random_select(request):
    if request.method == "GET":
        # 访问题目的时候创建一个session 保存当前的时间戳
        last = int(time.time())
        request.session["last_time"] = last
        count = Select.objects.all().count()

        if count < settings.RANDOM_SELECT:
            db = Select.objects.all()
        else:
            rand_ids = random.sample(range(1, count+1), settings.RANDOM_SELECT)
            db = Select.objects.filter(id__in=rand_ids)
        db = list(db)
        random.shuffle(db)
        return render(request, "random_select.html", {"data": db})


@login_required(login_url="login")
def selects(request):
    """
    多选题
    :param request: 必要参数
    :return: render
    """
    if request.method == "GET":
        last = int(time.time())
        request.session["last_time"] = last
        db = Selects.objects.all()
        return render(request, "selects.html", {"data": db})
    elif request.method == "POST":
        keys = request.POST.getlist("select")
        if not keys:
            return HttpResponse("你倒是选择啊.")
        db = Selects.objects
        true_total = 0
        pass_total = 0
        pass_key = []  # 做错的题号
        pass_value = []
        pass_index = []
        temp_index = []
        keys_true = {str(i.id): [i for i in i.key] for i in db.all()}  # 获得正确答案
        temp = {}

        for i in keys:
            key, value, indexkey = i.split("|")
            if str(key) not in temp.keys():
                temp[key] = []

            temp[key].append(value)
            temp_index.append(indexkey)

        temp_index = [int(i) for i in list(set(temp_index))]
        temp_index.sort()

        for i, j in zip(temp, temp_index):
            if operator.eq(temp[str(i)], keys_true[str(i)]):
                true_total += 1
            else:
                pass_total += 1
                pass_key.append(i)
                pass_value.insert(0, temp[str(i)])
                pass_index.insert(0, str(j))

        # 错误页面题号排序
        int_temp_index = [int(i) for i in pass_index]
        int_temp_index.sort(reverse=True)

        error_topic = [db.get(id=i) for i in pass_key]
        # error_topic = db.filter(id__in=pass_key)

        end_time = int(time.time())
        train_time = end_time - request.session["last_time"]

        # 修改数据库的内容
        request.user.userinfo.fraction += train_time
        request.user.userinfo.total += true_total + pass_total
        request.user.userinfo.ttotal += true_total
        request.user.userinfo.ftotal += pass_total
        request.user.userinfo.save()

        # count: 一共做了多少题目
        response = render(request, "error_pic.html", {
            'count': true_total + pass_total,
            'true_total': true_total,
            'pass_total': pass_total,
            'pass_key': pass_key,
            'error_topic': error_topic,
            'total': db.count(),
            'true_key': ["".join(i) for i in pass_value],
            'bfb': "%.2f" % (
                    int(true_total) / int(true_total + pass_total) * 100),
            'dual': True, 'time': train_time,
            'pass_index': int_temp_index
        })

        return response

    else:
        return HttpResponse("No")


@login_required(login_url="login")
def random_selects(request):
    if request.method == "GET":
        # 访问题目的时候创建一个session 保存当前的时间戳
        last = int(time.time())
        request.session["last_time"] = last
        count = Selects.objects.all().count()
        if count < settings.RANDOM_SELECTS:
            db = Selects.objects.all()
        else:
            rand_ids = random.sample(range(1, count+1), settings.RANDOM_SELECTS)
            db = Selects.objects.filter(id__in=rand_ids)

        db = list(db)
        random.shuffle(db)
        return render(request, "random_selects.html", {"data": db})


@login_required(login_url="login")
def judge(request):
    """
    判断题
    :param request: 必备参数
    :return: render
    """

    if request.method == "GET":
        last = int(time.time())
        request.session["last_time"] = last
        data = Judge.objects.all()
        return render(request, "judge.html", {"data": data})

    elif request.method == "POST":
        keys = request.POST.getlist("judge")
        # 判断是否没有做任何题目就点击了提交.
        if not keys:
            return HttpResponse("你倒是做题啊...")
        db = Judge.objects.all()
        true_total = 0  # 做对的题目数量
        pass_total = 0  # 做错的题目数量
        pass_key = []  # 做错的题号
        pass_value = []  # 做错的答案
        pass_index = []  # 错误索引
        keys_true = {str(i.id): i.key for i in db.all()}  # 正确答案

        temp = ""  # 用来检测一道题目是否选择了多个选项
        replace_temp = {"1": "对", "0": "错"}
        for i in keys:
            key, value, indexkey = i.split("|")
            if key == temp:
                return HttpResponse(f"检测到你第{indexkey}题选择了多个答案, 这次不分析成绩, 请重新开始.")
            temp = key
            if str(int(keys_true[str(key)])) == str(value):
                true_total += 1
            else:
                pass_total += 1
                pass_key.append(key)
                pass_value.insert(0, replace_temp[value])
                pass_index.append(indexkey)

        error_topic = [db.get(id=i) for i in pass_key]
        # error_topic = db.filter(id__in=pass_key)

        pass_index.sort(reverse=True)

        # 错误页面题号排序
        int_temp_index = [int(i) for i in pass_index]
        int_temp_index.sort(reverse=True)

        end_time = int(time.time())
        train_time = end_time - request.session["last_time"]

        # 修改数据库的内容
        request.user.userinfo.fraction += train_time
        request.user.userinfo.total += true_total + pass_total
        request.user.userinfo.ttotal += true_total
        request.user.userinfo.ftotal += pass_total
        request.user.userinfo.save()

        response = render(request, "error_pic.html", {
            "count": true_total + pass_total,
            "true_total": true_total,
            "pass_total": pass_total,
            "pass_key": pass_key,
            "error_topic": error_topic,
            "total": db.count(),
            "true_key": pass_value,
            "bfb": "%.2f" % (
                    int(true_total) / int(true_total + pass_total) * 100),
            "time": train_time,
            "pass_index": int_temp_index
        })

        return response

    else:
        return HttpResponse("No")


@login_required(login_url="login")
def random_judge(request):
    if request.method == "GET":
        # 访问题目的时候创建一个session 保存当前的时间戳
        last = int(time.time())
        request.session["last_time"] = last
        count = Judge.objects.all().count()
        if count < settings.RANDOM_JUDGE:
            db = Judge.objects.all()
        else:
            rand_ids = random.sample(range(1, count), settings.RANDOM_JUDGE)
            db = Judge.objects.filter(id__in=rand_ids)

        db = list(db)
        random.shuffle(db)
        return render(request, "random_judge.html", {"data": db})


def bugs(request):
    if request.method == "GET":
        data = Bugs.objects.order_by("-id")
        return render(request, "bugs.html", {
            "data": data,
        })


@login_required(login_url="login")
def create_user(request):
    if request.method == "GET":
        # 判断是否登陆
        # 判断是否为超级管理员
        if not request.user.is_superuser:
            return redirect("/")

        if os.path.exists("users.csv") is not True:
            return HttpResponse(f"请检查根目录是否存在'users.csv'文件~")

        data = pandas.read_csv("users.csv")
        for i, j in zip(data["username"], data["password"]):
            User.objects.create_user(f"{i}", None, f"{j}")

        return HttpResponse(f"创建完毕, 创建了{len(data['username'])}个用户.")

    else:
        return redirect("/")

def insert(request):


    return HttpResponse("success")




