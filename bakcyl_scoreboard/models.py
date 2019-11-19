from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    link = models.URLField()
    name = models.CharField(max_length=120, default=None)
    max_score = models.PositiveIntegerField()

    def __str__(self):
        return self.name

from django.utils.deconstruct import deconstructible

@deconstructible
class Score(models.Model):
    mark = models.PositiveIntegerField(default=0)
    comment = models.TextField(default='')
    tutor = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    isScored=models.BooleanField(default=False)

class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    code = models.TextField(default='')
    score = models.ForeignKey(Score, on_delete=models.CASCADE, default=Score())
    # isFinal = models.BooleanField(default=False)

    def __str__(self):
        return self.task.name + " " + self.user.username

    
