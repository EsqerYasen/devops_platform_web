from braces.views import *
from django.views.generic import *
from django.core.paginator import Paginator
from common.utils.redis_utils import *
from devops_platform_web.settings import PER_PAGE
from common.utils.HttpUtils import *

import logging

logger = logging.getLogger('devops_platform_log')

class List3View(LoginRequiredMixin, OrderableListMixin, ListView):
    #paginate_by = PER_PAGE
    template_name = "host_list_3.html"
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['']

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(List3View, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            host = reqData.get('host', None)
            if host:
                host = json.loads(host)
                host['go_live'] = 3
                reqData['host'] = host
            else:
                reqData['host'] = {'go_live': 3}
            tree = reqData.get('tree', None)
            if tree:
                reqData['tree'] = json.loads(tree)
            resultJson = hu.post(serivceName="cmdb", restName="/rest/host/list/", datas=reqData)
            resultJson = resultJson.json()
            list = resultJson.get("results", [])
            #hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/host/host_group_list/", datas={})
            hostGroup_list = RedisBase.get("host_group_3", 2)
            count = resultJson.get("count", 0)
            paginator = Paginator(list, req.limit)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
            context['hostGroup_list'] = hostGroup_list
        except Exception as e:
            logger.error(e, exc_info=1)
        return context


class Host3DetailView(LoginRequiredMixin, TemplateView):
    template_name = "host_detail3.html"

    def get_context_data(self, **kwargs):
        context = super(Host3DetailView, self).get_context_data(**kwargs)
        hu = HttpUtils(self.request)
        result = hu.post(serivceName="cmdb", restName="/rest/host/id_list/", datas={'host_id': [kwargs.get('pk')]})
        list = result.json().get("result", [])
        if list:
            context['host_info'] = list[0]
        else:
            context['host_info'] = {}
        return context

class Host3UpdateGoLiveView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
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
                    seach['go_live'] = 3
                    resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas=seach)
                    list = resultJson.get("results", [])
                    for l in list:
                        reqParam.append({'go_live': go_live, 'host_ip': l.get("host_ip")})

                updateResult = hu.post(serivceName="cmdb", restName="/rest/host/update/", datas=reqParam)
                result = updateResult.json()
                if result['status'] == '0':
                    result_json = {"status": 0}
        except Exception as e:
            logger.error(e,exc_info=1)
        return self.render_json_response(result_json)