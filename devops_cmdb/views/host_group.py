from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
import logging

logger = logging.getLogger('devops_platform_log')

class HostGroupView(LoginRequiredMixin, OrderableListMixin, TemplateView):
    template_name = "host_group.html"

    def get_context_data(self, **kwargs):
        context = super(HostGroupView, self).get_context_data(**kwargs)
        try:
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hu = HttpUtils(self.request)
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            context['hostGroup_list'] =  hostgroupResult.get("data", [])
        except Exception as e:
            logger.error(e)
        return context