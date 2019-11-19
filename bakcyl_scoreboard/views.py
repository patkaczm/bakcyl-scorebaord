from django.shortcuts import render
from django.http import HttpResponse
from .models import Task, Solution, Score
from django.contrib.auth.models import User
from .forms import SolutionForm

def index(request):
    tasks = Task.objects.all()
    return render(request, "bakcyl_scoreboard/dashboard.html", {"tasks":tasks})

def task_detail(response, task_id):
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
        return render(response, "bakcyl_scoreboard/task_detail.html", {"task":task,
                                                                      "solution":solution})
    else:
        return render(response, "bakcyl_scoreboard/task_detail.html", {"task":task,
                                                                      "solution":solution,
                                                                      "form":form})