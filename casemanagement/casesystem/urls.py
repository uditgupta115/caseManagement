from django.http import Http404
from django.urls import path
from django.views.defaults import page_not_found

from casemanagement.casesystem import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name='home_view'),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.user_logout, name='logout'),
    path("manager/", views.ManagerView.as_view(), name='manager_view'),
    path("task-manager/", views.TaskManagerView.as_view(), name='manager_view'),
    path("404/", page_not_found, {'exception': Exception(Http404)}),
    ]
