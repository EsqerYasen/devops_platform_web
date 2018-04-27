from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging

logger = logging.getLogger('devops_platform_log')

class DevopsToolsListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "devops_tools_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        try:
            context['result_list'] = []
        except Exception as e:
            logger.error(e)
        return context


class DevopsToolsCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "devops_tools_add.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            context["result_dict"] = {}
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            pass
        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')