from django.shortcuts import render, redirect
from register.models import PersonalInfo
import requests
from django.http import JsonResponse
from django.contrib.auth.models import User

def getUserTasksData(user):
    ret_data = {}

    codewars_nick = PersonalInfo.objects.get(user=user).codewars_name
    tasks = requests.get('https://www.codewars.com/api/v1/users/{}/code-challenges/completed'.format(codewars_nick)).json()['data']

    for task in tasks:
        if "cpp" in task["completedLanguages"]:
            task_rank = -requests.get('https://www.codewars.com/api/v1/code-challenges/{}'.format(task['id'])).json()["rank"]["id"]

            if not task_rank in ret_data:
                ret_data[task_rank] = []

            ret_data[task_rank].append({"name": task["name"],
                                        "time": task["completedAt"]})

    ret = []
    for kyu in sorted(ret_data.keys()):
        ret.append({
            "kyu": kyu,
            "tasks": ret_data[kyu]
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