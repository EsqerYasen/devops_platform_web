from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging,time,os

logger = logging.getLogger('devops_platform_log')

class DevopsFlowListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "flow_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(DevopsAppMgeListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            app_list_result = hu.get(serivceName="job", restName="/rest/app/list_app/", datas=reqData)
            app_list = app_list_result.get("results", {})
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


class DevopsFlowCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "app_deploy_form.html"

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
            version_list_str = reqData.get("version_list",None)
            addAppResults = hu.post(serivceName="job", restName="/rest/app/add_app/", datas=reqData)
            addAppResults = addAppResults.json()
            if addAppResults['status'] == 'SUCCESS':
                app_id = addAppResults['data']
                version_list = json.loads(version_list_str)
                appVersionResults = hu.post(serivceName="job", restName="/rest/app/update_app_version/", datas={'app_id':app_id,'version':version_list})
                appVersion = appVersionResults.json()
                if appVersion['status'] == 'SUCCESS':
                    result['status'] = 0
                    result['msg'] = '保存应用信息成功'
                else:
                    result['status'] = 1
                    result['msg'] = '保存应用版本信息失败'
            else:
                result['status'] = 1
                result['msg'] = '保存应用信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')