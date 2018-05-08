from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
import logging,time,os

logger = logging.getLogger('devops_platform_log')

class DevopsAppMgeListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "app_deploy_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(DevopsAppMgeListView, self).get_context_data(**kwargs)
        try:
            context['result_list'] = [{'id':1,'name':'Nginx'}]
        except Exception as e:
            logger.error(e)
        return context

class DevopsAppMgeCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "app_deploy_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            context["result_dict"] = {}
            context['is_add'] = 1
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()

        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class DevopsAppMgeUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "app_deploy_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            hu = HttpUtils(self.request)
            context['is_add'] = 0
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()

        except Exception as e:
            result['status'] = 1
            result['msg'] = '更新异常'
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')


class DevopsAppMgeDeleteView(LoginRequiredMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            req = self.request
            id = req.GET.get("id", 0)
            hu = HttpUtils(req)

        except Exception as e:
            result['status'] = 1
            result['msg'] = '删除异常'
            logger.error(e)
        return self.render_json_response(result)


class DevopsAppMgeDeployView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "app_deploy.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            id = kwargs.get('pk',0)
            name = req.GET.get('name',"")
            context["result_dict"] = {}
            context['is_add'] = 1
            context['name'] = name
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()

        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class GetCommandSetInfoView(LoginRequiredMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        result = []
        try:
            req = self.request
            hu = HttpUtils(req)
            name = req.GET.get('name',None)
            if name:
                resultJson = hu.get(serivceName="job", restName="/rest/job/list/", datas={'name': name})
                result = resultJson.get("results", [])
        except Exception as e:
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')