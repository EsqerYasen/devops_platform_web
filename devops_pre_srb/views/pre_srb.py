from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse, StreamingHttpResponse
from django.core.paginator import Paginator
from devops_platform_web.settings import DEVOPSGROUP,PRE_SRB_ADDITIONAL,PRE_SRB_ADDITIONAL_PERCENT
import logging,os,datetime,pptx
from django.conf import settings
from rest_framework.views import APIView
from .upload_download import readFile,remove_old_files

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
            reqData['is_auditor'] = 1
            resultJson = hu.get(serivceName="presrb", restName="/rest/presrb/project_list/", datas=reqData)
            list = resultJson.get("results", [])
            paginator = Paginator(list, req.limit)
            count = resultJson.get("count", 0)
            paginator.count = count
            is_auditor = 1
            # if req.devopsgroup == DEVOPSGROUP:
            #     is_auditor = 1
            context['is_auditor'] = is_auditor
            context['result_list'] = list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
            file_list = []
            for parent, dirnames, filenames in os.walk(settings.FILES_DIR):
                for filename in filenames:
                    file_list.append(filename)

            context['file_list'] = file_list
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
            #result = {"applicant":user.username,"applicant_email":user.email}
            result = {"applicant": user.username}
            context['result'] = result
            is_auditor = 1
            # if self.request.devopsgroup == DEVOPSGROUP:
            #     is_auditor = 1
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
        context['type'] = int(type)
        readonly = ""
        display = "block"
        if int(type) > 0:
            readonly = "readonly"
            display = "none"
        context['readonly'] = readonly
        context['display'] = display
        is_auditor = 1
        # if self.request.devopsgroup == DEVOPSGROUP:
        #     is_auditor = 1
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

            dt = get_device_dict(resultJson)
            if not is_one_2_one(dt):
                resultJson['env_level'] = "S-"

        except Exception as e:
            resultJson["status"] = 500
            resultJson["msg"] = "生成报表信息异常"
            logger.error(e,exc_info=1)
        return HttpResponse(json.dumps(resultJson), content_type='application/json')

class ProjectPptReportView(APIView):
    def get(self, request):
        resultJson = {}
        try:
            req = self.request
            id = int(req.GET.get('id', 0))

            if not os.path.exists(settings.FILES_CACHE_DIR):
                os.makedirs(settings.FILES_CACHE_DIR)

            hu = HttpUtils(req)
            resultJson = hu.get(serivceName="presrb", restName="/rest/presrb/project_report_item/", datas={"id":id})
            ppt_name = generate_ppt_report(resultJson)

            filepath = os.path.join(settings.FILES_CACHE_DIR, ppt_name)
            filename =ppt_name.split('_')[1]

            response = StreamingHttpResponse(readFile(filepath))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
                filename.encode('utf-8').decode('ISO-8859-1'))
            remove_old_files(settings.FILES_CACHE_DIR)
        except Exception as e:
            logger.error(e, exc_info=1)

        return response



def generate_ppt_report(info):
    try:
        dst_ppt_name = "ProjectReport.pptx"
        template_pptx_name = "template.pptx"

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        dst_ppt_name = nowTime + '_' + dst_ppt_name

        project_name = "项目名: %s" % info['name']
        project_online = "项目上线时间: %s " % info['estimated_pilot_date']
        project_info = "项目合计需求资源：    服务器台数:%s台 / 内存: %s G /  CPU: %s C /  硬盘: %s G (系统自动计算)" % (
            info['server_sum'], info['memory_sum'], info['cpu_sum'], info['disk_sum'])

        dt = get_device_dict(info)

        dt['level'] = '评级: %s级' % info['level']
        dt['project_info'] = project_name + "\n" + project_online + "\n" + project_info
        if not is_one_2_one(dt):
            additional_info = "(灾备环境和生产环境比例非1:1, 请注意风险)"
            dt['level'] += additional_info

        pptFile = pptx.Presentation(os.path.join(settings.PPTX_DIR, template_pptx_name))

        # change value for text box
        for shape in pptFile.slides[0].shapes:
            if shape.shape_type == 17 or shape.shape_type == 1:
                key = shape.name
                shape.text = str(dt[key])

        pptFile.save(os.path.join(settings.FILES_CACHE_DIR, dst_ppt_name))
    except Exception as e:
        logger.error(e, exc_info=1)
    return dst_ppt_name


def is_one_2_one(dict_info):
    flag = True
    if dict_info["product_text_num"] > 0:
        if dict_info['product_text_num'] > dict_info['disaster_text_num'] or \
                dict_info['product_text_mem'] > dict_info['disaster_text_mem'] or \
                dict_info['product_text_cpu'] > dict_info['disaster_text_cpu'] or \
                dict_info['product_text_disk'] > dict_info['disaster_text_disk']:
            flag=False
    return flag



def get_device_dict(dict_info):
    map2env = {
        1: "product",
        2: "disaster",
        3: "gray",
        4: "mainten",
    }
    dt = dict()
    # initail dict_info
    for i in range(1, 5):
        category = map2env[i]
        dt['%s_text_num' % category] = 0
        dt['%s_text_mem' % category] = 0
        dt['%s_text_cpu' % category] = 0
        dt['%s_text_disk' % category] = 0
    for items in dict_info['items']:
        env = items['env']
        category = map2env[env]
        dt['%s_text_num' % category] = items['estimated_server_count']
        dt['%s_text_mem' % category] = items['estimated_singleton_memory_capacity']
        dt['%s_text_cpu' % category] = items['estimated_singleton_CPU_core']
        dt['%s_text_disk' % category] = items['estimated_singleton_disk_capacity']
    return dt
