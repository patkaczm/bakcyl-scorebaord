from django.shortcuts import render, redirect
from .forms import RegisterForm
from bakcyl_scoreboard import urls as bakcyl_urls
from django.contrib.auth import authenticate, login
from .models import PersonalInfo

def register(response):
    if response.user.is_authenticated:
        return redirect("dashboard")
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            new_user = form.save()

            personal_info = PersonalInfo()
            personal_info.user = new_user
            personal_info.slack_name = form.cleaned_data['slack_username']
            personal_info.codewars_name = form.cleaned_data['codewars_username']
            personal_info.first_name = form.cleaned_data['first_Name']
            personal_info.last_name = form.cleaned_data['last_Name']
            personal_info.save()

            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(response, new_user)
            
            return redirect("dashboard")
    else:
        form = RegisterForm()
    
    return render(response, "register/register.html", {"form": form})