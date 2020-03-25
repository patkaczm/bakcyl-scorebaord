from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CwTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cwId = models.CharField(default="", max_length=120)
    completedAt = models.DateTimeField()
    kyu = models.PositiveIntegerField()
    name = models.CharField(default="", max_length=120)

    def __str__(self):
        return self.name + " " + self.user.username
