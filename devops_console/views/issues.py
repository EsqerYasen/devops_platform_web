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
            context['result_list'] = [{"issues_id":1,"jira_project_key":"test1","issue_type":"issue_type",
                                       "issue_summary":"issue_summary","issue_priority":"issue_priority",
                                       "issue_reporter":"issue_reporter","issue_status":"1","issue_create_date":"2018"}]
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


class IssuesDetailView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "issues_detail.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(IssuesDoneListView, self).get_context_data(**kwargs)
        try:
            pass
        except Exception as e:
            logger.error(e)
        return context