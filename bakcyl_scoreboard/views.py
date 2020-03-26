from django.shortcuts import render, redirect
from register.models import PersonalInfo
import requests
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import CwTask


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

    data = getUserTasksData(request.user)
    points = calculatePoints(data)

    return render(request, "bakcyl_scoreboard/dashboard.html", {
        "task_data": data,
        "points": points
    })


def all_users_data(request):
    ret = []
    for user in User.objects.all():
        if not PersonalInfo.objects.get(user=user).isTutor:
            all_user_kyus = [kyu["kyu"] for kyu in CwTask.objects.filter(user__personalinfo__isTutor=False).filter(user=user).order_by().values('kyu').distinct()]
            details = {}

            for kyu in all_user_kyus:
                count_ = CwTask.objects.all().filter(kyu=kyu).filter(user=user).count()
                if count_ > 0:
                    details[kyu] = count_

            pi = PersonalInfo.objects.get(user=user)
            ret.append({"name": "{} {}".format(pi.first_name, pi.last_name),
                       "kyuCount": details})
    return JsonResponse(ret, safe=False)


def task_kyu_count(request):
    all_kyus = [kyu["kyu"] for kyu in CwTask.objects.order_by().values('kyu').distinct()]
    ret = []

    for kyu in all_kyus:
        count_ = CwTask.objects.all().filter(user__personalinfo__isTutor=False).filter(kyu=kyu).count()
        if count_ > 0:
            ret.append({
                "kyu": kyu,
                "count": count_,
                "unique": CwTask.objects.all().filter(user__personalinfo__isTutor=False).filter(kyu=kyu).order_by().values('name').distinct().count(),
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

    students = PersonalInfo.objects.filter(isTutor=False)
    selectedStudent = None

    if request.method == "POST":
        if "showStatisticsUser" in request.POST:
            selectedStudent = request.POST.get("showStatisticsUser")

    return render(request, "bakcyl_scoreboard/dashboard_tutor.html", {
                                                                        "students":students,
                                                                        "selectedStudent": selectedStudent,
                                                                    })