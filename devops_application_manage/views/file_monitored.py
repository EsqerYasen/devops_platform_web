from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.core.paginator import Paginator
from django.http import HttpResponse
import logging

logger = logging.getLogger('devops_platform_log')

class FileMonitoredView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "file_monitored_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(FileMonitoredView, self).get_context_data(**kwargs)
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            inotify_result = hu.get(serivceName="cmdb", restName="/rest/inotify/list/",datas=reqData)
            inotify_list = inotify_result.get("results", [])
            context['result_list'] = list
            count = inotify_result.get("count", 0)
            paginator = Paginator(inotify_list, self.request.limit)
            paginator.count = count
            context['result_list'] = inotify_list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(self.request.offset)
            context['paginator'] = paginator
        except Exception as e:
            logging.error(e)
        return context


class FileMonitoredConfigListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "file_monitored_config_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(FileMonitoredConfigListView, self).get_context_data(**kwargs)
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            inotify_result = hu.get(serivceName="cmdb", restName="/rest/inotify/monitoritemlist/", datas=reqData)
            inotify_list = inotify_result.get("results", [])
            context['result_list'] = list
            count = inotify_result.get("count", 0)
            paginator = Paginator(inotify_list, self.request.limit)
            paginator.count = count
            context['result_list'] = inotify_list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(self.request.offset)
            context['paginator'] = paginator
        except Exception as e:
            logging.error(e)
        return context

class FileMonitoredConfigCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "file_monitored_config_add.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            context['hostGroup_list'] = hostgroupResult.get("data", [])
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            pass
        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')