import jwt
from django.contrib.auth import logout, login
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from casemanagement.casesystem.custom_middleware import get_verify_jwt_token
from casemanagement.casesystem.models import Roles


def user_logout(request):
    loggout_out = logout(request)
    del request.session['_auth_user']
    if loggout_out:
        return HttpResponse('You were logged out from session')
    return HttpResponse('unable to logout from session')


class LoginView(View):
    template_name = 'casesystem/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        role = request.role
        if role == Roles.MANAGER:
            return redirect(to='/manager/')
        elif role == Roles.TASK_MANAGER:
            return redirect(to='/task-manager/')
        else:
            return HttpResponse("Bad Role for user %s " % request.user)


class HomePageView(View):
    template_name = 'casesystem/index.html'

    def get(self, request, *args, **kwargs):
        if not request.user or isinstance(request.user, AnonymousUser):
            return redirect('/login/')
        role = request.role
        if role == Roles.MANAGER:
            return redirect(to='/manager/')
        elif role == Roles.TASK_MANAGER:
            return redirect(to='/task-manager/')
        else:
            return HttpResponse("Bad Role for user %s " % request.user)


class ManagerView(TemplateView):
    template_name = 'casesystem/index.html'

    def get(self, request, *args, **kwargs):
        if request.session.has_key('_auth_user'):
            auth_hash = request.session['_auth_user']
            # if auth_hash:
            #     verify_token = get_verify_jwt_token(
            #         request.user.token_secret_key,
            #         auth_hash,
            #         True
            #     )
                # if verify_token:
            return render(request, self.template_name, {"username": request.user})
        else:
            return redirect('/login/')


class TaskManagerView(TemplateView):
    template_name = 'casesystem/taskmanager_home.html'





