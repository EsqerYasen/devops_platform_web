from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator

import logging,json
logger = logging.getLogger('devops_platform_log')

class VIPListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "vip_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            vipAddJson = hu.get(serivceName="cmdb", restName="/rest/vip/", datas=reqData)
            list = vipAddJson.get("results", [])
            for l in list:
                hostResult = hu.get(serivceName="cmdb",restName="/rest/host/list_host_by_vip",datas={"vip":l.get("name","")})
                l['iplist'] = hostResult.get("data",[])
            paginator = Paginator(list, req.limit)
            count = vipAddJson.get("count", 0)
            paginator.count = count
            context['resultList'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context

class VIPCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    def post_ajax(self, request, *args, **kwargs):
        result = {}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            vipAddResult = hu.post(serivceName="cmdb", restName="/rest/vip_add/", datas={"name":reqData["name"],"key_code":reqData["key_code"],"virtual_router_id":reqData["virtual_router_id"]})
            vipAdd = vipAddResult.json()
            if vipAdd['status'] == "SUCCESS":
                result['status'] = 0
            else:
                result['status'] = 1
                result['msg'] = "新增VIP失败"
        except Exception as e:
            result['status'] = 1
            result['msg'] = "新增VIP异常"
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class VIPBindIPView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    def post_ajax(self, request, *args, **kwargs):
        result = {}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            iplist = json.loads(reqData.get("ipList",[]))
            id = reqData.get("id",None)
            result['total'] = len(iplist)
            success = 0
            fail = 0
            if id:
                for ip in iplist:
                    hostResult = hu.get(serivceName="cmdb",restName="/rest/host/",datas={"host_ip":ip})
                    host = hostResult.get("results",None)
                    if host:
                        host_id = host[0].get("id",None)
                        if host_id:
                            bindVipJson = hu.get(serivceName="cmdb", restName="/rest/host/bind_vip/",datas={"vip_id": id, "host_id": host_id,"type":2})
                            #bindVipJson = bindVipResult.json()
                            if bindVipJson['status'] == "SUCCESS":
                                success += 1;
                            else:
                                fail += 1;
                result['success'] = 1
                result['fail'] = 1
                result['status'] = 0
            else:
                result['status'] = 1
                result['success'] = 0
                result['fail'] = 0
                result['msg'] = "绑定失败"
        except Exception as e:
            result['status'] = 1
            result['success'] = 0
            result['fail'] = 0
            result['msg'] = "绑定失败"
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')
