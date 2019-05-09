from django.shortcuts import render, HttpResponse
from kaoshi.models import Select, Selects, Judge
import operator
import time
import random

# Create your views here.


def index(request):
    train_time = request.COOKIES.get("t")
    if train_time is None:
        response = render(request, "welcome.html")
        response.set_cookie('t', 0)

    else:
        total = int(request.COOKIES.get("t")) / 60
        response = render(request, "welcome.html", {"total": "%.2f" % total})

    return response


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
        if keys == []:
            return HttpResponse("你倒是选择啊.")
        db = Select.objects
        true_total = 0  # 做对的题目数量
        pass_total = 0  # 做错的题目数量
        pass_key = []  # 做错的题号
        pass_value = []  # 做错的答案
        pass_index = []  # 错误索引
        keys_true = {str(i.id):i.key for i in db.all()}  # 正确答案
        temp = ""
        for i in keys:
            key, value, indexkey = i.split("|")
            if key == temp:
                return HttpResponse(f"检测到你第{temp}题选择了多个答案, 这次不分析成绩, 请重新开始.")
            temp = key
            if keys_true[str(key)] == value:
                true_total += 1
            else:
                pass_total += 1
                pass_value.append(value)
                pass_key.append(key)
                pass_index.append(indexkey)  # 错误的索引

        error_topic = db.filter(id__in=pass_key)
        pass_value.sort(reverse=True)
        pass_index.sort(reverse=True)

        # 提交题目, 获取当前的时间戳，并获取之前看到题目的时间戳, 进行减法运算, 得到时间.
        end_time = int(time.time())
        train_time = end_time - request.session["last_time"]
        request.session["train_time"] = train_time

        # return HttpResponse(11)
        # count: 一共做了多少题目
        response = render(request, "error_pic.html", {"count": true_total + pass_total,
                                                  "true_total": true_total,
                                                  "pass_total": pass_total,
                                                  "pass_key": pass_key,
                                                  "error_topic": error_topic,
                                                  "total": db.count(),
                                                  "true_key": pass_value,
                                                  "bfb": "%.2f" % (int(true_total) / int(true_total + pass_total) * 100),
                                                  "dual": True,
                                                  "time": train_time,
                                                  "pass_index": pass_index,
                                                  })

        if request.COOKIES.get("t"):
            temp_time = int(request.COOKIES.get("t")) if int(request.COOKIES.get("t")) else 0
        else:
            temp_time = 0
        temp_time += train_time
        response.set_cookie('t', temp_time)
        return response
    else:
        return HttpResponse("No")

def random_select(request):
    if request.method == "GET":
        # 访问题目的时候创建一个session 保存当前的时间戳
        last = int(time.time())
        request.session["last_time"] = last
        count = Select.objects.all().count()
        rand_ids = random.sample(range(1, count), 50)
        db = Select.objects.filter(id__in=rand_ids)
        return render(request, "random_select.html", {"data": db})

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
        if keys == []:
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

        print(temp_index)
        temp_index = list(set(temp_index))
        temp_index.sort()

        for i, j in zip(temp, temp_index):
            if operator.eq(temp[str(i)], keys_true[str(i)]):
                true_total += 1
            else:
                pass_total += 1
                pass_key.append(i)
                pass_value.append(temp[str(i)])
                pass_index.insert(0, j)

        # 错误页面题号排序
        int_temp_index = [int(i) for i in pass_index]
        int_temp_index.sort(reverse=True)

        error_topic = db.filter(id__in=pass_key)
        pass_value.sort()

        end_time = int(time.time())
        train_time = end_time - request.session["last_time"]
        request.session["train_time"] = train_time


        # count: 一共做了多少题目
        response = render(request, "error_pic.html", {"count": true_total + pass_total,
                                                  "true_total": true_total,
                                                  "pass_total": pass_total,
                                                  "pass_key": pass_key,
                                                  "error_topic": error_topic,
                                                  "total": db.count(),
                                                  "true_key": ["".join(i) for i in pass_value],
                                                  "bfb": "%.2f" % (int(true_total) / int(true_total + pass_total) * 100),
                                                  "dual": True,
                                                  "time": train_time,
                                                  "pass_index": int_temp_index,
                                                  })

        if request.COOKIES.get("t"):
            temp_time = int(request.COOKIES.get("t")) if int(request.COOKIES.get("t")) else 0
        else:
            temp_time = 0
        temp_time += train_time
        response.set_cookie('t', temp_time)
        return response

    else:
        return HttpResponse("No")

def random_selects(request):
    if request.method == "GET":
        # 访问题目的时候创建一个session 保存当前的时间戳
        last = int(time.time())
        request.session["last_time"] = last
        count = Selects.objects.all().count()
        rand_ids = random.sample(range(1, count), 15)
        db = Selects.objects.filter(id__in=rand_ids)
        return render(request, "random_selects.html", {"data": db})

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
        if keys == []:
            return HttpResponse("你倒是做题啊...")
        db = Judge.objects.all()
        true_total = 0  # 做对的题目数量
        pass_total = 0  # 做错的题目数量
        pass_key = []  # 做错的题号
        pass_value = []  # 做错的答案
        pass_index = []  # 错误索引
        keys_true = {str(i.id):i.key for i in db.all()}  # 正确答案

        temp = ""  # 用来检测一道题目是否选择了多个选项
        for i in keys:
            key, value, indexkey = i.split("|")
            if key == temp:
                return HttpResponse(f"检测到你第{temp}题选择了多个答案, 这次不分析成绩, 请重新开始.")
            temp = key
            if str(int(keys_true[str(key)])) == str(value):
                true_total += 1
            else:
                pass_total += 1
                pass_key.append(key)
                pass_value.append(True if value == "1" else False)
                pass_index.append(indexkey)

        error_topic = db.filter(id__in=pass_key)
        pass_value = pass_value[::-1]
        replace_temp = {"True": "对", "False": "错"}
        pass_value = [replace_temp[str(i)] for i in pass_value]
        pass_index.sort(reverse=True)

        # 错误页面题号排序
        int_temp_index = [int(i) for i in pass_index]
        int_temp_index.sort(reverse=True)


        end_time = int(time.time())
        train_time = end_time - request.session["last_time"]
        request.session["train_time"] = train_time

        response = render(request, "error_pic.html", {"count": true_total + pass_total,
                                                  "true_total": true_total,
                                                  "pass_total": pass_total,
                                                  "pass_key": pass_key,
                                                  "error_topic": error_topic,
                                                  "total": db.count(),
                                                  "true_key": pass_value,
                                                  "bfb": "%.2f" % (int(true_total) / int(true_total + pass_total) * 100),
                                                  "time": train_time,
                                                      "pass_index": int_temp_index
                                                  })
        if request.COOKIES.get("t"):
            temp_time = int(request.COOKIES.get("t")) if int(request.COOKIES.get("t")) else 0
        else:
            temp_time = 0
        temp_time += train_time
        response.set_cookie('t', temp_time)
        return response

    else:
        return HttpResponse("No")

def random_judge(request):
    if request.method == "GET":
        # 访问题目的时候创建一个session 保存当前的时间戳
        last = int(time.time())
        request.session["last_time"] = last
        count = Judge.objects.all().count()
        rand_ids = random.sample(range(1, count), 15)
        db = Judge.objects.filter(id__in=rand_ids)
        return render(request, "random_judge.html", {"data": db})