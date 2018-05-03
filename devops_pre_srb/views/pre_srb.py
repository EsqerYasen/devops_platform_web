from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging

logger = logging.getLogger('devops_platform_log')

class PreSrbListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "pre_srb_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            # tool_list_result = hu.get(serivceName="job", restName="/rest/job/list_tool_set/",datas=reqData)
            # tool_list = tool_list_result.get("results", {})
            # for tool in tool_list:
            #     tool['param'] = json.loads(tool['param'])
            # paginator = Paginator(tool_list, req.limit)
            # count = tool_list_result.get("count", 0)
            # paginator.count = count
            # context['result_list'] = tool_list
            # context['is_paginated'] = count > 0
            # context['page_obj'] = paginator.page(req.offset)
            # context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


class PreSrbCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "pre_srb_add.html"

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
            # hu = HttpUtils(self.request)
            # reqData = hu.getRequestParam()
            # if reqData:
            #     addResult = hu.post(serivceName="job", restName="/rest/job/add_tool_set/", datas=reqData)
            #     addResultJson = addResult.json()
            #     if addResultJson['status'] == 'SUCCESS':
            #         result['status'] = 0
            #         result['msg'] = '保存成功'
            #     else:
            #         result['status'] = 1
            #         result['msg'] = '保存失败'
            # else:
            #     result['status'] = 1
            #     result['msg'] = '保存值为空'

        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')
