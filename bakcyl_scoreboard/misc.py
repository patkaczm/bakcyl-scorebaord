from .models import CwTask
from register.models import PersonalInfo
from django.contrib.auth.models import User
import requests

from background_task import background
@background()
def updateCwTasks():
    for pi in PersonalInfo.objects.all():
        user_tasks = requests.get('https://www.codewars.com/api/v1/users/{}/code-challenges/completed'.format(pi.codewars_name))
        user_tasks = user_tasks.json()
        if "data" in user_tasks:
            user_tasks = user_tasks['data']

            user_cw_tasks = CwTask.objects.filter(user=pi.user)
            for task in user_tasks:
                if "cpp" in task["completedLanguages"]:
                    if not user_cw_tasks.filter(cwId=task["id"]).exists():
                        cwTask = CwTask()
                        cwTask.user = pi.user
                        cwTask.name = task["name"]
                        cwTask.cwId = task["id"]
                        cwTask.completedAt = task["completedAt"]
                        cwTask.kyu = -requests.get('https://www.codewars.com/api/v1/code-challenges/{}'.format(task['id'])).json()["rank"]["id"]
                        cwTask.save()
        else:
            print("Data for {} not found".format(pi.codewars_name))