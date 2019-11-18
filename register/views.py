from django.shortcuts import render, redirect
from .forms import RegisterForm
from bakcyl_scoreboard import urls as bakcyl_urls

def register(response):

    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = RegisterForm()
    
    return render(response, "register/register.html", {"form": form})