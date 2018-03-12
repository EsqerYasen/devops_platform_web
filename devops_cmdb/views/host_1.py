from braces.views import *
from django.views.generic import *
from django.core.paginator import Paginator

from devops_platform_web.settings import PER_PAGE
from common.utils.HttpUtils import *

import logging

logger = logging.getLogger('devops_platform_log')

class ListView(LoginRequiredMixin, OrderableListMixin, ListView):
    paginate_by = PER_PAGE
    template_name = "host_list_1.html"
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['']

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            offset = int(req.GET.get('offset',1))
            offset2 = (offset - 1) * 10
            hu = HttpUtils()
            resultJson = hu.get(serivceName="cmdb", restName="/rest/host/", datas={'offset': offset2, 'limit': PER_PAGE,'go_live':1})
            list = resultJson.get("results",[])

            paginator = Paginator(resultJson.get("results",[]), PER_PAGE)
            count = resultJson.get("count",0)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context