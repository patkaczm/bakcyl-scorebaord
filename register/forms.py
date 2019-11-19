from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    slack_username = forms.CharField(max_length=40)
    codewars_username = forms.CharField(max_length=40)
    first_Name = forms.CharField(max_length=40)
    last_Name = forms.CharField(max_length=40)
    class Meta:
        model = User
        fields = ["username", "first_Name", "last_Name","email", "slack_username", 'codewars_username', "password1", "password2"]