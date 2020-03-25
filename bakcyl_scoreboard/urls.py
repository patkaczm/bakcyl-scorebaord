from django.urls import path
from . import views
from .misc import updateCwTasks

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user/all', views.all_users_data, name='all_user_data'),
    path('user/<username>', views.user_data, name='user_data'),
    path('dt', views.dashboard_tutor, name="dashboard_tutor"),
    path('task/kyu-count', views.task_kyu_count, name='task_kyu_count'),
    path('task/all', views.task_all, name='task_all'),
]



# should be run one a day
# from background_task.models import Task
# updateCwTasks(repeat=Task.DAILY)
# print("Tasks updated")