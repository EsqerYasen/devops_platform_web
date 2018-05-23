from braces.views import *
from django.views.generic import *
import logging

logger = logging.getLogger('devops_platform_log')

class List1View(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "file_monitored_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(List1View, self).get_context_data(**kwargs)
        try:
            pass
        except Exception as e:
            logging.error(e)
        return context