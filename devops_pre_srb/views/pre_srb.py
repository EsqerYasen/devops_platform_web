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
        context = super(PreSrbListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            resultJson = hu.get(serivceName="presrb", restName="/rest/presrb/project_list/", datas=reqData)
            list = resultJson.get("results", [])
            paginator = Paginator(list, req.limit)
            count = resultJson.get("count", 0)
            paginator.count = count
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


class PreSrbCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "pre_srb_add.html"

    def get_context_data(self, **kwargs):
        context = super(PreSrbCreateView, self).get_context_data(**kwargs)
        try:
            context["is_add"] = 1
            hu = HttpUtils(self.request)
            auditor_list = hu.get(serivceName="presrb", restName="/rest/presrb/auditor_list/", datas={})
            context['auditor_list'] = auditor_list
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            saveJson = reqData.get("saveJson",None);
            if saveJson:
                resultAdd = hu.post(serivceName="presrb", restName="/rest/presrb/project_add/", datas=saveJson)
                resultJson = resultAdd.json()
                if resultJson['status'] == 'SUCCESS':
                    result['status'] = 0
                    result['msg'] = '保存成功'
                else:
                    result['status'] = 1
                    result['msg'] = '保存失败'
            else:
                result['status'] = 1
                result['msg'] = '保存值为空'

        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class PreSrbUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "pro_assess_add/pro_assess.html"

    def get_context_data(self, **kwargs):
        context = super(PreSrbUpdateView, self).get_context_data(**kwargs)
        context["is_add"] = 1
        id = self.argsp[0]
        if id:
            hu = HttpUtils()
            auditor_list = hu.get(serivceName="presrb", restName="/rest/presrb/auditor_list/",datas={})
            context['auditor_list'] = auditor_list

            category_list = hu.get(serivceName="presrb", restName="/rest/presrb/category_list/", datas={})
            context['category_list'] = category_list

            resultJson = hu.get(serivceName="presrb", restName="/rest/presrb/project_list_item/", datas={"id": id})
            data = resultJson.get("data", [])
            context['result'] = data

        return context

    def post(self, request, *args, **kwargs):
        saveJson = request.POST.get("saveJson",None);

        hu = HttpUtils()
        resultJson = hu.post(serivceName="presrb", restName="/rest/presrb/project_add/", datas=saveJson)

        return HttpResponse(json.dumps(resultJson.json()),content_type='application/json')
