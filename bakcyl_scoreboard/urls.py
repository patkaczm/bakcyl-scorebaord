from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('task/<int:task_id>/', views.task_detail, name='detail'),
]
