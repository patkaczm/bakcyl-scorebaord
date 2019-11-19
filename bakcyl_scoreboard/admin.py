from django.contrib import admin
from .models import *

class SolutionAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'isFinal')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_score')


admin.site.register(Task, TaskAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Score)
