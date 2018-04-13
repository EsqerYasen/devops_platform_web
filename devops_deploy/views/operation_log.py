from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging

logger = logging.getLogger('devops_platform_log')

class OperationLogView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "operation_log.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            historyListResult = hu.get(serivceName="job", restName="/rest/deploy/history_list/", datas=reqData)
            historyList = historyListResult.get("results", [])

            paginator = Paginator(historyList, req.limit)
            count = historyListResult.get("count", 0)
            paginator.count = count
            context['result_list'] = historyList
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context