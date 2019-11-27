from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task, Solution, Score
from django.contrib.auth.models import User
from .forms import SolutionForm, CommentForm, TaskForm
from register.models import PersonalInfo

def get_tasks(user):
    userGroupLevel = PersonalInfo.objects.get(user=user).group_level
    
    tasks = {"all":Task.objects.all(),
             "mandatory":{
                "done":[],
                "notdone":[],
             },
             "obligatory":{
                 "done":[],
                 "notdone":[],
             },
             }

    for t in Task.objects.all():
        if t.group_level == userGroupLevel:
            try:
                Solution.objects.get(user=user, task=t, isFinal=True)
                tasks['mandatory']['done'].append(t)
            except:
                tasks['mandatory']['notdone'].append(t)
        else:
            try:
                Solution.objects.get(user=user, task=t, isFinal=True)
                tasks['obligatory']['done'].append(t)
            except:
                tasks['obligatory']['notdone'].append(t)
    return tasks

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
        form = SolutionForm(response.POST)
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
    
    tasks = get_tasks(response.user)

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

def add_task(response):
    if (response.method == 'POST'):
        form = TaskForm(response.POST)
        if (form.is_valid()):
            task = Task()
            task.group_level = form.cleaned_data['group_level']
            task.link = form.cleaned_data['link']
            task.max_score = form.cleaned_data['max_score']
            task.name = form.cleaned_data['name']
            task.save()
            return redirect("add_task")

    form = TaskForm()
    return render(response, "bakcyl_scoreboard/add_task.html", {
                                                                "tasks":Task.objects.all(),
                                                                "form":form})