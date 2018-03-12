from braces.views import *
from django.views.generic import *
from devops_platform_web.settings import PER_PAGE
import logging
from django.core.paginator import Paginator
from common.utils.HttpUtils import *

logger = logging.getLogger('devops_platform_log')

class CommandSetListView(LoginRequiredMixin, OrderableListMixin, ListView):
    paginate_by = PER_PAGE
    template_name = "command_set_list.html"
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['']

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(CommandSetListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            offset = int(req.GET.get('offset', 1))

            hu = HttpUtils()
            offset2 = (offset - 1)*10
            resultJson = hu.get(serivceName="job", restName="/rest/job/list/", datas={'offset': offset2, 'limit': PER_PAGE})
            list = resultJson.get("results", [])

            paginator = Paginator(resultJson.get("results", []), PER_PAGE)
            count = resultJson.get("count", 0)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


