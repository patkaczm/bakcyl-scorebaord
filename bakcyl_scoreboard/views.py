from django.shortcuts import render, redirect
from register.models import PersonalInfo


def dashboard(response):
    if not response.user.is_authenticated:
        return redirect("login")

    return render(response, "bakcyl_scoreboard/dashboard.html")


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