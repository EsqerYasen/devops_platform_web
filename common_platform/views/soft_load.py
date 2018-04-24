from braces.views import *
from django.views.generic import *
import logging

logger = logging.getLogger('devops_platform_log')

class SoftLoadView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "soft_load_page.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(SoftLoadView, self).get_context_data(**kwargs)
        try:
            pass
        except Exception as e:
            logger.error(e)
        return context