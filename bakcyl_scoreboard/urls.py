from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user/<user_name>', views.user_dashboard, name='user_dashboard'),
    path('dt', views.dashboard_tutor, name="dashboard_tutor"),
]
