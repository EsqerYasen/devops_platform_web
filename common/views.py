#-*- coding: UTF-8 -*-
from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

# from common.utils.ldap3_api import *

from common.utils.HttpUtils import *
from django.conf import settings
import logging,time

logger = logging.getLogger('devops_platform_log')

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
    redirect_url = "/?type=1"
    try:
        method = request.method
        bool = True
        username = ""
        if method == "GET":
            code = request.GET.get('code',None)
            if code:
                tokendata = settings.TOKEN_DATA
                tokendata['code'] = code
                tokendata['oauth_timestamp'] = time.time()
                hu = HttpUtils(request)
                result = hu.get_url(settings.OAUTH_TOKEN, tokendata)
                if result.status_code == 200:
                    access_token = result.json()['access_token']
                    userinfo_result = hu.get_url(settings.OAUTH_USERINFO, {"access_token": access_token})
                    userinfo = userinfo_result.json()
                    username = userinfo['yumADAccount'].lower()
                    bool = True
        elif method == "POST":
            username = request.POST.get('username',None)
            password = request.POST.get('password',None)
            if username and password:
                bool = AdAuthenticate.authenricate(username,password)
        if bool:
            user = auth.authenticate(username=username, password=settings.USER_DEFAULT_PWD)
            if user and user.is_active:
                auth.login(request, user)
                redirect_url = '/mainform/'
                logger.info("user '" + username + "' authentication through")
    except Exception as e:
        logging.error(e)
    return redirect(redirect_url)


def logout(request):
    auth.logout(request)
    return redirect('/?type=2')


def mainform(request):
    """
    系统主窗体
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return render(request, 'common/mainform.html', {})
    else:
        return redirect('/?type=1')

def dashboard(request):

    return render(request, 'common/dashboard.html', {
        'module': ""
    })
