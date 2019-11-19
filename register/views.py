from django.shortcuts import render, redirect
from .forms import RegisterForm
from bakcyl_scoreboard import urls as bakcyl_urls
from django.contrib.auth import authenticate, login

def register(response):

    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(response, new_user)
            
            return redirect("dashboard")
    else:
        form = RegisterForm()
    
    return render(response, "register/register.html", {"form": form})