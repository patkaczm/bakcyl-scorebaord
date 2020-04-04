from django.shortcuts import render, redirect
from register.models import PersonalInfo
import requests
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import CwTask
import datetime
from .misc import updateTasksForUser, updateCwTaskss


def getUserTasksData(user):
    kyus = set()
    for task in CwTask.objects.filter(user=user):
        kyus.add(task.kyu)

    ret = []
    for kyu in sorted(kyus):
        ret.append({
            "kyu": kyu,
            "tasks": [task.name for task in CwTask.objects.filter(user=user).filter(kyu=kyu)]
        })
    return ret


def calculatePoints(tasks):
    points = 0
    for task in tasks:
        points += len(task["tasks"]) * (100 - (10 * task["kyu"]))
    return points


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        if request.POST.get('refresh') == 'refresh':
            updateTasksForUser(request.user)

    data = getUserTasksData(request.user)
    points = calculatePoints(data)

    return render(request, "bakcyl_scoreboard/dashboard.html", {
        "task_data": data,
        "points": points
    })


def get_user_data(user, dateFrom, dateTo, filterTutor = True):
    if filterTutor and PersonalInfo.objects.get(user=user).isTutor:
        return
    else:
        all_user_kyus = [kyu["kyu"] for kyu in CwTask.objects.filter(
            user=user).order_by().values('kyu').distinct()]
        details = {}

        for kyu in all_user_kyus:
            if isinstance(dateFrom, datetime.date) and isinstance(dateTo, datetime.date):
                count_ = CwTask.objects.all().filter(kyu=kyu).filter(
                    completedAt__range=(dateFrom, dateTo)).filter(user=user).count()
            else:
                count_ = CwTask.objects.all().filter(kyu=kyu).filter(user=user).count()
            if count_ > 0:
                details[kyu] = count_

        pi = PersonalInfo.objects.get(user=user)
        return {"name": "{} {}".format(pi.first_name, pi.last_name),
                "kyuCount": details}


def all_users_data(request):
    ret = []
    for user in User.objects.all():
        data = get_user_data(user, None, None)
        if data:
            ret.append(data)
    return JsonResponse({'data': ret})


def last_week_users_data(request):
    today = datetime.date.today()
    last_week_monday = today - datetime.timedelta(days=today.weekday(), weeks=1)
    last_week_sunday = last_week_monday + datetime.timedelta(days=6)

    ret = []
    for user in User.objects.all():
        data = get_user_data(user, last_week_monday, last_week_sunday)
        if data:
            ret.append(data)


    return JsonResponse({
        'data': ret,
        'time': {
            'start': last_week_monday,
            'end': last_week_sunday,
        }})


def this_week_users_data(request):
    today = datetime.date.today()
    this_week_monday = today - datetime.timedelta(days=today.weekday())
    this_week_sunday = this_week_monday + datetime.timedelta(days=6)

    ret = []
    for user in User.objects.all():
        data = get_user_data(user, this_week_monday, this_week_sunday)
        if data:
            ret.append(data)

    return JsonResponse({
        'data': ret,
        'time': {
            'start': this_week_monday,
            'end': this_week_sunday,
        }
    })


def this_week_user_data(request, username):
    today = datetime.date.today()
    this_week_monday = today - datetime.timedelta(days=today.weekday())
    this_week_sunday = this_week_monday + datetime.timedelta(days=6)

    user = User.objects.get(username=username)
    data = get_user_data(user, this_week_monday, this_week_sunday, False)

    return JsonResponse({
        'data': data,
        'time': {
            'start': this_week_monday,
            'end': this_week_sunday,
        }
    })

def task_kyu_count(request):
    all_kyus = [kyu["kyu"] for kyu in CwTask.objects.order_by().values('kyu').distinct()]
    ret = []

    for kyu in all_kyus:
        count_ = CwTask.objects.all().filter(user__personalinfo__isTutor=False).filter(kyu=kyu).count()
        if count_ > 0:
            ret.append({
                "kyu": kyu,
                "count": count_,
                "unique": CwTask.objects.all().filter(user__personalinfo__isTutor=False).filter(
                    kyu=kyu).order_by().values('name').distinct().count(),
            })

    return JsonResponse(ret, safe=False)


def task_all(request):
    all_taks_names = [name["name"] for name in CwTask.objects.order_by().values('name').distinct()]
    ret = []

    for name in all_taks_names:
        count_ = CwTask.objects.all().filter(user__personalinfo__isTutor=False).filter(name=name).count()
        if count_ > 0:
            ret.append({
                "name": name,
                "kyu": CwTask.objects.filter(name=name)[0].kyu,
                "count": count_
            })

    return JsonResponse(ret, safe=False)


def user_data(request, username):
    user = User.objects.get(username=username)
    return JsonResponse(getUserTasksData(user), safe=False)


def points(request):
    students = User.objects.filter(personalinfo__isTutor=False)
    ret = []
    for student in students:
        pi = PersonalInfo.objects.get(user=student)
        tasks = CwTask.objects.filter(user=student)
        score = 0
        for task in tasks:
            score += 100 - (10 * task.kyu)
        ret.append({
            "name": "{} {}".format(pi.first_name, pi.last_name),
            "points": score
        })
    return JsonResponse(ret, safe=False)


def dashboard_tutor(request):
    if not request.user.is_authenticated:
        return redirect("login")

    isTutor = PersonalInfo.objects.get(user=request.user).isTutor
    if not isTutor:
        return redirect("dashboard")

    if request.method == "POST":
        if request.POST.get('refresh') == 'refresh':
            print("clicked")
            updateCwTaskss()

    students = PersonalInfo.objects.filter(isTutor=False)
    selectedStudent = None

    if request.method == "POST":
        if "showStatisticsUser" in request.POST:
            selectedStudent = request.POST.get("showStatisticsUser")

    return render(request, "bakcyl_scoreboard/dashboard_tutor.html", {
        "students": students,
        "selectedStudent": selectedStudent,
    })
