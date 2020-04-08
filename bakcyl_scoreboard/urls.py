from django.urls import path
from . import views
from .misc import updateCwTasks

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user/all', views.all_users_data, name='all_user_data'),
    path('user/last-week', views.last_week_users_data, name='last_week_users_data'),
    path('user/this-week', views.this_week_users_data, name='this_week_users_data'),
    path('user/<username>/this-week', views.this_week_user_data, name='this_week_user_data'),
    path('user/<username>/last-week', views.last_week_user_data, name='last_week_user_data'),
    path('user/score', views.points, name='score_all'),
    path('user/<username>', views.user_data, name='user_data'),
    path('dt', views.dashboard_tutor, name="dashboard_tutor"),
    path('task/kyu-count', views.task_kyu_count, name='task_kyu_count'),
    path('task/all', views.task_all, name='task_all'),
]



# should be run one a day
# from background_task.models import Task
# updateCwTasks(repeat=Task.DAILY)
# print("Tasks updated")