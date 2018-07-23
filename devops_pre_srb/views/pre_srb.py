from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from devops_platform_web.settings import DEVOPSGROUP,PRE_SRB_ADDITIONAL,PRE_SRB_ADDITIONAL_PERCENT
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
            is_auditor = 0
            if req.devopsgroup == DEVOPSGROUP:
                is_auditor = 1
            context['is_auditor'] = is_auditor
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e,exc_info=1)
        return context


class PreSrbCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "pre_srb_add.html"

    def get_context_data(self, **kwargs):
        context = super(PreSrbCreateView, self).get_context_data(**kwargs)
        try:
            context["is_add"] = 1
            context['readonly'] = ""
            context['display'] = "block"
            context['type'] = 0
            user = self.request.user
            result = {"applicant":user.username,"applicant_email":user.email}
            context['result'] = result
            is_auditor = 0
            if self.request.devopsgroup == DEVOPSGROUP:
                is_auditor = 1
            context['is_auditor'] = is_auditor
            hu = HttpUtils(self.request)
            auditor_list = hu.get(serivceName="presrb", restName="/rest/presrb/auditor_list/", datas={})
            context['auditor_list'] = auditor_list
            # category_list = hu.get(serivceName="presrb", restName="/rest/presrb/category_list/", datas={})
            # context['category_list'] = category_list
            categoryItem_list = hu.get(serivceName="presrb", restName="/rest/presrb/categoryItem_list/", datas={})
            context['categoryItem_list'] = categoryItem_list
            context['pre_srb_additional'] = PRE_SRB_ADDITIONAL
            context['pre_srb_additional_percent'] = PRE_SRB_ADDITIONAL_PERCENT
        except Exception as e:
            logger.error(e,exc_info=1)
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
                    result['p_id'] = resultJson.get("p_id","")
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
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result),content_type='application/json')



class PreSrbUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "pro_assess_add/pro_assess.html"

    def get_context_data(self, **kwargs):
        context = super(PreSrbUpdateView, self).get_context_data(**kwargs)
        context["is_add"] = 1
        id = kwargs.get('pk', 0)
        type = self.request.GET.get("type",0)
        context['type'] = type
        readonly = ""
        display = "block"
        if int(type) > 0:
            readonly = "readonly"
            display = "none"
        context['readonly'] = readonly
        context['display'] = display
        is_auditor = 0
        if self.request.devopsgroup == DEVOPSGROUP:
            is_auditor = 1
        context['is_auditor'] = is_auditor
        context['pre_srb_additional'] = PRE_SRB_ADDITIONAL
        context['pre_srb_additional_percent'] = PRE_SRB_ADDITIONAL_PERCENT
        if id:
            hu = HttpUtils(self.request)
            auditor_list = hu.get(serivceName="presrb", restName="/rest/presrb/auditor_list/",datas={})
            context['auditor_list'] = auditor_list

            categoryItem_list = hu.get(serivceName="presrb", restName="/rest/presrb/categoryItem_list/", datas={})
            context['categoryItem_list'] = categoryItem_list

            resultJson = hu.get(serivceName="presrb", restName="/rest/presrb/project_byid/", datas={"id": id})
            data = {}
            if resultJson['status'] == 200:
                data = resultJson['data']
            context['result'] = data

        return context

    def post(self, request, *args, **kwargs):
        result = {}
        try:
            id = kwargs.get('pk', 0)
            if id:
                saveJson = request.POST.get("saveJson", None);
                hu = HttpUtils(request)
                update_result = hu.post(serivceName="presrb", restName="/rest/presrb/project_update/", datas=saveJson)
                result_json = update_result.json()
                result['p_id'] = id
                if result_json['status'] == 'SUCCESS':
                    result['status'] = 0
                    result['msg'] = '保存成功'
                else:
                    result['status'] = 1
                    result['msg'] = "更新失败"
            else:
                result['status'] = 1
                result['msg'] = "更新主键为空"
        except Exception as e:
            result['status'] = 1
            result['msg'] = "更新异常"
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(result),content_type='application/json')

class ProjectUpdateStatusView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        resultJson = {}
        try:
            req_get = request.GET
            hu = HttpUtils(request)
            resultJson1 = hu.post(serivceName="presrb", restName="/rest/presrb/project_status_update/", datas={"p_id":req_get['p_id'],"status":req_get['status']})
            resultJson = resultJson1.json()
        except Exception as e:
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(resultJson), content_type='application/json')

class  ProjectItemCreateView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        resultJson = {}
        try:
            saveJson = request.POST.get("saveJson", None)
            saveJson = eval(saveJson)
            hu = HttpUtils(request)
            # updateResult = hu.post(serivceName="presrb", restName="/rest/presrb/project_update/", datas={"p_id":saveJson.get("p_id",0),"deploy_envs":saveJson.get("deploy_envs",0),"change":0})
            # updateJson = updateResult.json()
            # if updateJson.get("status") == "SUCCESS":
            #     resultJson1 = hu.post(serivceName="presrb", restName="/rest/presrb/projectItem_add/", datas=saveJson)
            #     resultJson2 = resultJson1.json()
            #     if resultJson2.get("status") == "SUCCESS":
            #         resultJson["status"] = 0
            #     else:
            #         resultJson["status"] = 1
            #         resultJson["msg"] = "保存应用配置失败"

            resultJson1 = hu.post(serivceName="presrb", restName="/rest/presrb/projectItem_add/", datas=saveJson)
            resultJson2 = resultJson1.json()
            if resultJson2.get("status") == "SUCCESS":
                resultJson["status"] = 0
            else:
                resultJson["status"] = 1
                resultJson["msg"] = "保存应用配置失败"

        except Exception as e:
            resultJson["status"] = 1
            resultJson["msg"] = "保存应用配置异常"
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(resultJson), content_type='application/json')


class ProjectItemListView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        results = {}
        try:
            id = request.GET.get("id",None)
            if id:
                hu = HttpUtils(request)
                resultJson = hu.get(serivceName="presrb", restName="/rest/presrb/project_item_list/", datas={"p_id": id})
                results["data"] = resultJson.get("data", [])
                results["status"] = 200
            else:
                results["status"] = 500
                results["data"] = []
        except Exception as e:
            results["status"] = 500
            logger.error(e, exc_info=1)
        return HttpResponse(json.dumps(results), content_type='application/json')

class ProjectReportView(LoginRequiredMixin,JSONResponseMixin, AjaxResponseMixin, View):

    def get_ajax(self, request, *args, **kwargs):
        resultJson = {}
        try:
            req = self.request
            id = int(req.GET.get('id', 0))
            hu = HttpUtils(req)
            resultJson = hu.get(serivceName="presrb", restName="/rest/presrb/project_report_item/", datas={"id":id})
        except Exception as e:
            resultJson["status"] = 500
            resultJson["msg"] = "生成报表信息异常"
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(resultJson), content_type='application/json')