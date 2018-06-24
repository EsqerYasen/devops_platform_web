from braces.views import *
from django.views.generic import *
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from djqscsv import render_to_csv_response
from devops_platform_web.settings import PER_PAGE,BASE_DIR
from common.utils.HttpUtils import *
from devops_auth.models import *
from django.core import serializers
from django.contrib.auth.models import User


import logging,os,xlrd,threading,re

logger = logging.getLogger('devops_platform_log')

class AuthListView(LoginRequiredMixin, OrderableListMixin, ListView):
    # 权限查看和管理
    #paginate_by = PER_PAGE
    template_name = "auth.html"
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['']

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        req = self.request
        hu = HttpUtils(req)
        # reqData = hu.getRequestParam()
        # json = hu.get(serivceName="auth", restName="/manager/list/", datas=reqData)
        # list = json.get("results", [])
        # for l in list:
        #     hostResult = hu.get(serivceName="auth",restName="/rest/host/list_host_by_vip",datas={"vip":l.get("name","")})
        #     l['iplist'] = hostResult.get("data",[])
        # paginator = Paginator(list, req.limit)
        # count = json.get("count", 0)
        # paginator.count = count
        # context['resultList'] = list
        # context['is_paginated'] = count > 0
        # context['page_obj'] = paginator.page(req.offset)
        # context['paginator'] = paginator
        try:
            req = self.request
            # hu = HttpUtils(req)
            # reqData = hu.getRequestParam()
            # json = hu.get(serivceName="auth", restName="/manager/list/", datas=reqData)
            # list = json.get("results", [])
            # for l in list:
            #     hostResult = hu.get(serivceName="auth",restName="/rest/host/list_host_by_vip",datas={"vip":l.get("name","")})
            #     l['iplist'] = hostResult.get("data",[])
            # paginator = Paginator(list, req.limit)
            # count = json.get("count", 0)
            # paginator.count = count
            # context['resultList'] = list
            # context['is_paginated'] = count > 0
            # context['page_obj'] = paginator.page(req.offset)
            # context['paginator'] = paginator
            # context['userid'] = req.user
            context['userid'] = req.user.id;
            context['user'] = json.dumps({"admin": req.user.is_superuser, "userid":req.user.id});
        except Exception as e:
            logger.error(e)
        # context['user'] = serializers.serialize('json',  [req.user])
        return context