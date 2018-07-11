from braces.views import *
from django.views.generic import *
from common.utils.redis_utils import *
import logging,json

logger = logging.getLogger('devops_platform_log')

class HostDashboardView(LoginRequiredMixin, OrderableListMixin,JSONResponseMixin,AjaxResponseMixin, ListView):
    template_name = "host_dashboard.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(HostDashboardView, self).get_context_data(**kwargs)
        return context

    def post_ajax(self, request, *args, **kwargs):
        results = {}
        try:
            reqPost = self.request.POST
            key = reqPost.get("key", None)
            if key:
                results['status'] = 200
                results['data'] = json.loads(str(RedisBase.get(key, 2),encoding='utf-8'))
            else:
                results['status'] = 500
                results['data'] = []
        except Exception as e:
            results['status'] = 500
            logger.error(e,exc_info=1)
        return self.render_json_response(results)
