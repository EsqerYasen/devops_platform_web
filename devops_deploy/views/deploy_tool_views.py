from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging,time,os

logger = logging.getLogger('devops_platform_log')

class DeployToolListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "deploy_tool_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(DeployToolListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            app_list_result = hu.get(serivceName="job", restName="/rest/deploytool/list/", datas=reqData)
            app_list = app_list_result.get("results", {})
            for app in app_list:
                app_list_result = hu.get(serivceName="job", restName="/rest/deploytool/versionlist/", datas={"deploy_id":app['id']})
                app['version_list'] = app_list_result.get("data",[])
            count = app_list_result.get("count", 0)
            paginator = Paginator(app_list, req.limit)
            paginator.count = count
            context['result_list'] = app_list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


class DeployToolCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "deploy_tool_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            context['version_list'] = []
            context['app_info'] = {}
            context['is_add'] = 1
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            addAppResults = hu.post(serivceName="job", restName="/rest/deploytool/add/", datas=reqData)
            addAppResults = addAppResults.json()
            if addAppResults['status'] == 'SUCCESS':
                result['status'] = 0
                result['msg'] = '保存发布信息成功'
            else:
                result['status'] = 1
                result['msg'] = '保存发布信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class DeployToolUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "deploy_tool_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            id = kwargs.get('pk', 0)
            hu = HttpUtils(self.request)
            app_list_result = hu.get(serivceName="job", restName="/rest/deploytool/list/", datas={'id':id})
            app_list = app_list_result.get("results", {})
            app = {}
            if len(app_list) > 0:
                app = app_list[0]
            context['app_info'] = app
            context['is_add'] = 0
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            app_id = reqData.get("id", None)
            if app_id:
                del reqData['offset']
                del reqData['limit']
                del reqData['csrfmiddlewaretoken']
                addAppResults = hu.post(serivceName="job", restName="/rest/deploytool/update/", datas=reqData)
                addAppResults = addAppResults.json()
                if addAppResults['status'] == 'SUCCESS':
                    result['status'] = 0
                    result['msg'] = '更新发版信息成功'
                else:
                    result['status'] = 1
                    result['msg'] = '更新发版信息失败'
            else:
                result['status'] = 1
                result['msg'] = '更新发版信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '更新异常'
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')