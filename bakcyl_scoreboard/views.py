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
    solutuion = None
    if response.method == "POST":
        if "showSolution" in response.POST:
            solutuion = Solution.objects.get(id=response.POST.get("showSolution"))
        elif "submit" in response.POST:
            form = CommentForm(response.POST)
            if form.is_valid():
                scored_solution = Solution.objects.get(id=response.POST.get("submit"))
                score = scored_solution.score
                score.comment = form.cleaned_data['comment']
                score.mark = form.cleaned_data['score']
                score.tutor = response.user
                score.isScored = True
                score.save()
                print(scored_solution)
        else:
            pass
            

    all_tasks = Task.objects.all()
    task = Task.objects.get(id=task_id)
    unscored = Solution.objects.filter(task=task, score__isScored=False, isFinal=True)
    scored = Solution.objects.filter(task=task, score__isScored=True, isFinal=True)
    
    form = CommentForm()

    return render(response, "bakcyl_scoreboard/task_detail_tutor.html", {"tasks":all_tasks,
                                                                         "task":task,
                                                                         "form":form,
                                                                         "scored":scored,
                                                                         "unscored":unscored,
                                                                         "solution":solutuion})

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
    
    tasks_done = []
    tasks_notdone = []
    for t in Task.objects.all():
        try:
            Solution.objects.get(user=response.user, task=t, isFinal=True)
            tasks_done.append(t)
        except:
            tasks_notdone.append(t)

    tasks = {"all":Task.objects.all(),
             "done":tasks_done,
             "notdone":tasks_notdone}

    if solution and solution.isFinal:
        return render(response, "bakcyl_scoreboard/task_detail.html", {
                                                                    "tasks":Task.objects.all(),
                                                                    "task":task,
                                                                    "solution":solution,
                                                                    "all":tasks
                                                                    })
    else:
        return render(response, "bakcyl_scoreboard/task_detail.html", {
                                                                    "tasks":Task.objects.all(),
                                                                    "task":task,
                                                                    "solution":solution,
                                                                    "form":form,
                                                                    "all":tasks})

def task_detail(response, task_id):
    isTutor = PersonalInfo.objects.get(user=response.user).isTutor
    if not isTutor:
        return task_detail_user(response, task_id)
    else:
        return task_detail_tutor(response, task_id)