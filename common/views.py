#-*- coding: UTF-8 -*-
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from common.utils.ldap3_api import *
from common.utils.HttpUtils import *
from common.utils.redis_utils import *
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
        bool = False
        username = ""
        password = ""
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
            if username == 'admin':
                bool = True
            else:
                if username and password:
                    bool = AdAuthenticate.authenricate(username,password)
        if bool:
            if username == 'admin':
                user = auth.authenticate(username=username, password=password)
            else:
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


def hostTotalCount(request):
    results = {}
    try:
        r_key = "hostTotalCount_%s" % settings.DEVOPSGROUP
        result = RedisBase.get(redisKey=r_key,db=1)
        if result:
            results['status'] = 200
            results['data'] = json.loads(str(result,encoding="utf-8"))
        else:
            hu = HttpUtils(request)
            get_results = hu.get(serivceName="cmdb", restName="/rest/host/host_total_count/",datas={})
            if get_results['status'] == 200:
                data = get_results['data']
                RedisBase.set(redisKey=r_key,value=json.dumps(data),time_ms=120,db=1)
                results['status'] = 200
                results['data'] = data
            else:
                results['status'] = 500
    except Exception as e:
        results['status'] = 500
        logger.error(e,exc_info=1)
    return HttpResponse(json.dumps(results),content_type='application/json')


def page_not_found(request):
    return render(request, '404.html')

def page_error(request):
    return render(request, '500.html')

def page_forbidden(request):
    return render(request, '403.html')


def forward_to_service(request):
    results = {}
    try:
        method = request.method
        hu = HttpUtils(request)
        if method == "GET":
            req_get = request.GET
            serivceName = req_get.get("serivceName",None)
            restName = req_get.get("restName",None)
            req_data = req_get.get("req_data", None)
            if serivceName and restName:
                results = hu.get(serivceName=serivceName, restName=restName,datas=req_data)
            else:
                results['status'] = 500
        else:
            req_post = request.POST
            serivceName = req_post.get("serivceName", None)
            restName = req_post.get("restName", None)
            req_data = req_post.get("req_data", None)
            if serivceName and restName:
                p_result = hu.post(serivceName=serivceName, restName=restName,datas=req_data)
                results = json.dumps(p_result.json())
            else:
                results['status'] = 500
    except Exception as e:
        logger.error(e,exc_info=1)
        results['status'] = 500
    return HttpResponse(json.dumps(results), content_type='application/json')