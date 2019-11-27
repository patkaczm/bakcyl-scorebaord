from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('task/<int:task_id>/', views.task_detail, name='detail'),
    path('add_task', views.add_task, name='add_task'),
    path('task/all/data', views.maininfo_chart_data, name="maininfo_chart_data"),
    path('<user>/data/tasks', views.user_chart_data, name="user_chart_data"),
    path('task/<task_id>/data', views.task_chart_data, name="task_chart_data"),
    path('dt', views.dashboard_tutor, name="dashboard_tutor"),
]
