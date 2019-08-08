from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from casemanagement.casesystem.models import Roles, Case, Task


def user_logout(request):
    logout(request)
    return redirect('/login/')


class LoginView(View):
    template_name = 'casesystem/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return HttpResponse('Invalid Credentials')
        if user and not isinstance(user, AnonymousUser):
            login(request, user)

        if hasattr(user, 'userrole'):
            setattr(request, 'role', user.userrole.role)

        role = request.role
        if role == Roles.MANAGER:
            return redirect(to='/manager/')
        elif role == Roles.TASK_MANAGER:
            return redirect(to='/task-manager/')
        else:
            return redirect(to='/404/')


class HomePageView(View):
    template_name = 'casesystem/base.html'

    def get(self, request, *args, **kwargs):
        if not request.user or isinstance(request.user, AnonymousUser):
            return redirect('/login/')
        role = request.role
        if role == Roles.MANAGER:
            return redirect('/manager/')
        elif role == Roles.TASK_MANAGER:
            return redirect(to='/task-manager/')
        else:
            return HttpResponse("Bad Role for user %s " % request.user)


class ManagerView(TemplateView):
    template_name = 'casesystem/manager_home.html'

    def get(self, request, *args, **kwargs):

        cases = Case.objects.filter(role__user=request.user)

        context = {"username": request.user, 'cases': cases}
        #     # if auth_hash:
        #     #     verify_token = get_verify_jwt_token(
        #     #         request.user.token_secret_key,
        #     #         auth_hash,
        #     #         True
        #     #     )
        #     # if verify_token:
        return render(request, self.template_name, context)


class TaskManagerView(TemplateView):
    template_name = 'casesystem/taskmanager_home.html'

    def get(self, request, *args, **kwargs):

        tasks = Task.objects.filter(
            Q(role__user=request.user) | Q(case__role__user=request.user)
        ).distinct()
        context = {"username": request.user, 'tasks': tasks}
        return render(request, self.template_name, context)


class HelloView(View):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return HttpResponse('Hello, World!')
