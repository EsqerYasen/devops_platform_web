from braces.views import *
from django.views.generic import *

import logging
logger = logging.getLogger('devops_platform_log')

class IssuesListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "issues_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(IssuesListView, self).get_context_data(**kwargs)
        try:
            pass
        except Exception as e:
            logger.error(e)
        return context


class IssuesDoneListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "issues_list_done.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(IssuesDoneListView, self).get_context_data(**kwargs)
        try:
            pass
        except Exception as e:
            logger.error(e)
        return context