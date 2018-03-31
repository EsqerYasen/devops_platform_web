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

            treeResult = hu.get(serivceName="cmdb", restName="/rest/app/treeview/", datas={})

            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            brandResult = hu.get(serivceName="cmdb", restName="/rest/brands/", datas=getData)
            pidcResult = hu.get(serivceName="cmdb", restName="/rest/pidc/", datas=getData)
            lidcResult = hu.get(serivceName="cmdb", restName="/rest/lidc/", datas=getData)
            envResult = hu.get(serivceName="cmdb", restName="/rest/env/", datas=getData)
            mwResult = hu.get(serivceName="cmdb", restName="/rest/mw/", datas=getData)
            dnsResult = hu.get(serivceName="cmdb", restName="/rest/dns/", datas=getData)

            paginator = Paginator(resultJson.get("results",[]), req.limit)
            count = resultJson.get("count",0)
            paginator.count = count
            context['result_list'] = list
            context['tree_list'] = treeResult.get("data",[])
            context['brand_list'] = brandResult.get("results", [])
            context['pidc_list'] = pidcResult.get("results", [])
            context['lidc_list'] = lidcResult.get("results", [])
            context['env_list'] = envResult.get("results", [])
            context['mw_list'] = mwResult.get("results", [])
            context['dns_list'] = dnsResult.get("results", [])
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


class Host2RedistributionView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            flag = request.POST.get("flag",None);
            if flag:
                hu = HttpUtils(request)
                redistribution = json.loads(request.POST.get("redistribution"))
                redistribution['go_live'] = 2
                reqParam = []
                if flag == '1':
                    ip_list = json.loads(request.POST.get("ip_list"))
                    for ip in ip_list:
                        reqDict = redistribution.copy()
                        reqDict['host_ip'] = ip
                        reqParam.append(reqDict)
                else:
                    seach = json.loads(request.POST.get("seach", None))
                    seach['go_live'] = 2
                    resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas=seach)
                    list = resultJson.get("results", [])
                    for l in list:
                        reqDict = redistribution.copy()
                        reqDict['host_ip'] = l.get("host_ip")
                        reqParam.append(reqDict)

                updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=reqParam)
                result = updateResult.json()
                if result['status'] == '0':
                    result_json = {"status": 0}
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)


class Host2UpdateGoLiveView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        result_json = {"status": 1}
        try:
            flag = request.POST.get("flag",None);
            if flag:
                hu = HttpUtils(request)
                go_live = request.POST.get("status")
                reqParam = []
                if flag == '1':
                    ip_list = json.loads(request.POST.get("ip_list"))
                    for ip in ip_list:
                        reqParam.append({'go_live':go_live,'host_ip':ip})
                else:
                    seach = json.loads(request.POST.get("seach", None))
                    seach['go_live'] = 2
                    resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas=seach)
                    list = resultJson.get("results", [])
                    for l in list:
                        reqParam.append({'go_live': go_live, 'host_ip': l.get("host_ip")})

                updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=reqParam)
                result = updateResult.json()
                if result['status'] == '0':
                    result_json = {"status": 0}
        except Exception as e:
            logger.error(e)
        return self.render_json_response(result_json)