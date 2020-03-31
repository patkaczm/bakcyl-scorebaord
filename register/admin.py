from django.contrib import admin
from .models import *


class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'codewars_name', 'first_name', 'last_name', 'isTutor')


admin.site.register(PersonalInfo, PersonalInfoAdmin)