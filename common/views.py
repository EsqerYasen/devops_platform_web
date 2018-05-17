#-*- coding: UTF-8 -*-
from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

class LoginView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['type'] = self.request.GET.get('type', '')
        return context


def checkLogin(request):
    """
    登录校验，使用Django默认的用户权限模块
    :param request:
    :param authentication_form:
    :return:
    """

    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    print('authuser %s' % user)

    user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
    if user and user.is_active:
        auth.login(request, user)
        return redirect('/mainform/')
    else:
        return redirect('/?type=1')

def logout(request):
    auth.logout(request)
    return redirect('/?type=2')


def mainform(request):
    """
    系统主窗体
    :param request:
    :return:
    """
    return render(request, 'common/mainform.html', {})

def dashboard(request):

    return render(request, 'common/dashboard.html', {
        'module': ""
    })
