from django.db import models
from django.contrib.auth.models import User

class PersonalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slack_name = models.CharField(max_length=40, default='')
    codewars_name = models.CharField(max_length=40, default='')
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.user.username