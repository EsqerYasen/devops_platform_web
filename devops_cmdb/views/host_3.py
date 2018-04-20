from braces.views import *
from django.views.generic import *
from django.core.paginator import Paginator

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
            type = req.GET.get("type", 0)
            list = []
            if type == '2':
                group_id = reqData.get("group_id", 0)
                resultJson = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_host_sp/",
                                    datas={"id": group_id, "go_live": 3,"offset":reqData.get("offset",0),"limit":reqData.get("limit")})
                resultListLeader = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_leader/",
                                          datas={"id": group_id})
                listLeader = resultListLeader.get("data", [])
                ops = listLeader.get("ops", [])
                opsStr = ""
                for o in ops:
                    if o:
                        opsStr += o + ","
                developStr = ""
                develop = listLeader.get("develop", [])
                for d in develop:
                    if d:
                        developStr += d + ","
                list = resultJson.get("results", [])
            else:
                reqData['go_live'] = 3
                resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas=reqData)
                list = resultJson.get("results",[])
                for host in list:
                    apps = host.get("apps",[])
                    groupIds = []
                    for app in apps:
                        groupIds.append(str(app.get("group_id",0)))
                    resultListLeader = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_leader/", datas={"id":'+'.join(groupIds)})
                    listLeader = resultListLeader.get("data",[])
                    ops = listLeader.get("ops",[])
                    opsStr = ""
                    for o in ops:
                        if o:
                            opsStr += o+","
                    developStr = ""
                    develop = listLeader.get("develop",[])
                    for d in develop:
                        if d:
                            developStr += d+","
                    host['ops'] = opsStr
                    host['develop'] = developStr

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
            logger.error(e)
        return self.render_json_response(result_json)