from django.shortcuts import render
from django.http import HttpResponse
from .models import Task, Solution, Score
from django.contrib.auth.models import User
from .forms import SolutionForm, CommentForm
from register.models import PersonalInfo

def index(request):
    tasks = Task.objects.all()
    return render(request, "bakcyl_scoreboard/dashboard.html", {"tasks":tasks})

def task_detail_tutor(response, task_id):
    all_tasks = Task.objects.all()
    task = Task.objects.get(id=task_id)
    solutuions = Solution.objects.filter(task=task)
    form = CommentForm()
    if type(solutuions) == Solution:
        solutuions = [solutuions]

    return render(response, "bakcyl_scoreboard/task_detail_tutor.html", {"tasks":all_tasks,
                                                                         "form":form,
                                                                         "solutions":solutuions})
    pass

def task_detail_user(response, task_id):
    task = Task.objects.get(id=task_id)
        
    try:
        solution = Solution.objects.get(task=task, user=response.user)
    except:
        solution=None
    
    if response.method == "POST":
        form = form = SolutionForm(response.POST)
        if form.is_valid():
            if not solution:
                solution = Solution()
                score = Score()
                score.save()
                solution.score = score
                solution.task = task
                solution.user = response.user
            solution.code = form.cleaned_data['code']
            if "final" in response.POST:
                solution.isFinal = True
            solution.save()
    else:
        form = SolutionForm()
        
    if solution and solution.isFinal:
        return render(response, "bakcyl_scoreboard/task_detail.html", {
                                                                    "tasks":Task.objects.all(),
                                                                    "task":task,
                                                                    "solution":solution,
                                                                    })
    else:
        return render(response, "bakcyl_scoreboard/task_detail.html", {
                                                                    "tasks":Task.objects.all(),
                                                                    "task":task,
                                                                    "solution":solution,
                                                                    "form":form})

def task_detail(response, task_id):
    # isTutor = PersonalInfo.objects.get(user=response.user).isTutor
    isTutor = False
    if not isTutor:
        return task_detail_user(response, task_id)
    else:
        return task_detail_tutor(response, task_id)