from braces.views import *
from django.views.generic import *
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from djqscsv import render_to_csv_response
from devops_platform_web.settings import PER_PAGE,BASE_DIR
from common.utils.HttpUtils import *
from devops_menu.models import *
from django.core import serializers
from django.contrib.auth.models import User


import logging,os,xlrd,threading,re

logger = logging.getLogger('devops_platform_log')

class MenuListView(LoginRequiredMixin, OrderableListMixin, ListView):
    # 权限查看和管理
    #paginate_by = PER_PAGE
    template_name = "menu.html"
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['']

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        req = self.request
        hu = HttpUtils(req)
        try:
            req = self.request
            context['userid'] = req.user.id;
            context['user'] = json.dumps({"admin": req.user.is_superuser, "userid":req.user.id});
        except Exception as e:
            logger.error(e)
        # context['user'] = serializers.serialize('json',  [req.user])
        return context
