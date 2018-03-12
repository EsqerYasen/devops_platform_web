from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from devops_platform_web.settings import PER_PAGE
from django.core.paginator import Paginator
import logging

logger = logging.getLogger('devops_platform_log')

class BusinesAttributessView(LoginRequiredMixin, TemplateView):
    template_name = "business_attributes.html"

    def get_context_data(self, **kwargs):
        context = super(BusinesAttributessView, self).get_context_data(**kwargs)
        try:
            reqGet = self.request.GET
            tab = reqGet.get("tab", 0)
            offset = int(reqGet.get('offset', 1))
            resultJson = {}
            if tab == "0":
                resultJson = self.brandList(reqGet)
            elif tab == "1":
                resultJson = self.groupList(reqGet)
                context['brand_list'] = self.brandList({'offset': 1, 'limit': 1000, 'is_enabled': 1}).get("results", [])
            elif tab == "2":
                resultJson = self.moduleList(reqGet)
                context['brand_list'] = self.brandList({'offset': 1, 'limit': 1000, 'is_enabled': 1}).get("results", [])

            list = resultJson.get("results", [])
            paginator = Paginator(list, PER_PAGE)
            count = resultJson.get("count", 0)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(offset)
            context['paginator'] = paginator
            context['tab'] = tab
        except Exception as e:
            logger.error(e)
        return context

    def brandList(self, args):
        offset = int(args.get('offset', 1))
        limit = int(args.get('limit', 0))
        offset2 = (offset - 1) * PER_PAGE
        if limit == 0:
            limit = PER_PAGE

        getData = {'offset': offset2, 'limit': limit, 'is_enabled': 1}
        name = args.get('name', None)
        if name:
            getData['name'] = name
        hu = HttpUtils()
        resultJson = hu.get(serivceName="appcenter", restName="/rest/brands/", datas=getData)
        return resultJson

    def groupList(self,args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE,'is_enabled':1}
        name = args.get('name', None)
        if name:
            getData['name']=name
        biz_brand_id = args.get('biz_brand_id', None)
        if biz_brand_id:
            getData['biz_brand']=biz_brand_id
        hu = HttpUtils()
        resultJson = hu.get(serivceName="appcenter", restName="/rest/groups/", datas=getData)
        return resultJson

    def moduleList(self,args):
        offset = int(args.get('offset', 1))
        offset2 = (offset - 1) * PER_PAGE
        getData = {'offset': offset2, 'limit': PER_PAGE,'is_enabled':1}
        name = args.get('name', None)
        if name:
            getData['name']=name
        biz_brand_id = args.get('biz_brand_id', None)
        if biz_brand_id:
            getData['biz_brand']=biz_brand_id
        biz_group_id = args.get('biz_group_id', None)
        if biz_group_id:
            getData['biz_group'] = biz_group_id
        hu = HttpUtils()
        resultJson = hu.get(serivceName="appcenter", restName="/rest/modules/",datas=getData)
        return resultJson