from casemanagement.casesystem import views
from django.urls import path


urlpatterns = [
    path("", views.HomePageView.as_view(), name='home_view'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.user_logout, name='logout'),
    path("manager/", views.ManagerView.as_view(), name='manager_view'),
    path("task-manager/", views.TaskManagerView.as_view(), name='manager_view')
    ]
