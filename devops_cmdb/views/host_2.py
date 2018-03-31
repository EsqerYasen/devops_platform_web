from braces.views import *
from django.views.generic import *
from django.core.paginator import Paginator

from devops_platform_web.settings import PER_PAGE
from common.utils.HttpUtils import *

import logging

logger = logging.getLogger('devops_platform_log')

class List2View(LoginRequiredMixin, OrderableListMixin, ListView):
    #paginate_by = PER_PAGE
    template_name = "host_list_2.html"
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['']

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(List2View, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            reqData['go_live'] = 2

            resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas=reqData)
            list = resultJson.get("results",[])

            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)

            paginator = Paginator(resultJson.get("results",[]), req.limit)
            count = resultJson.get("count",0)
            paginator.count = count
            context['result_list'] = list
            context['hostGroup_list'] = hostgroupResult.get("data", [])
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


class Host2DetailView(LoginRequiredMixin, TemplateView):
    template_name = "host_detail2.html"

    def get_context_data(self, **kwargs):
        context = super(Host2DetailView, self).get_context_data(**kwargs)
        hu = HttpUtils(self.request)
        result = hu.post(serivceName="cmdb", restName="/rest/host/id_list/", datas={'host_id': [kwargs.get('pk')]})
        list = result.json().get("result", [])
        if list:
            context['host_info'] = list[0]
        else:
            context['host_info'] = {}
        return context


class Host2UpdateGoLiveView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            flag = request.POST.get("flag",None);
            if flag:
                hu = HttpUtils(request)
                go_live = request.POST.get("status")
                reqParam = []
                ip_list = json.loads(request.POST.get("ip_list"))
                for ip in ip_list:
                    reqParam.append({'go_live': go_live, 'host_ip': ip})

                updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=reqParam)
                result = updateResult.json()
                if result['status'] == '0':
                    result_json = {"status": 0}
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)


class Host2BindingGroup(LoginRequiredMixin,JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            groupId = request.POST.get("group_id",None)
            host_ids = request.POST.get("host_ids",None)
            if groupId and host_ids:
                hu = HttpUtils(request)
                reqParam = {"group_id":groupId,"host_ids":host_ids}
                updateResult = hu.post(serivceName="cmdb", restName="/rest/host/hostgroup/static_group_append/", datas=reqParam)
                result = updateResult.json()
                if len(result) > 0:
                    result_json = {"status": 0}
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)


class Host2UnbundlingGroup(LoginRequiredMixin,JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            groupId = request.POST.get("group_id",None)
            host_ids = request.POST.get("host_ids",None)
            if groupId and host_ids:
                hu = HttpUtils(request)
                reqParam = {"group_id":groupId,"host_ids":host_ids}
                updateResult = hu.post(serivceName="cmdb", restName="/rest/host/hostgroup/static_group_delete/", datas=reqParam)
                result = updateResult.json()
                if len(result) > 0:
                    result_json = {"status": 0}
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)