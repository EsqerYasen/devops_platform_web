from braces.views import *
from django.views.generic import *
from common.utils.HttpUtils import *
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
import logging,time,os

logger = logging.getLogger('devops_platform_log')

class DevopsFlowListView(LoginRequiredMixin, OrderableListMixin, ListView):
    template_name = "flow_list.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(DevopsFlowListView, self).get_context_data(**kwargs)
        try:
            req = self.request
            hu = HttpUtils(req)
            reqData = hu.getRequestParam()
            app_list_result = hu.get(serivceName="job", restName="/rest/flowcontrol/list/", datas=reqData)
            app_list = app_list_result.get("results", {})
            count = app_list_result.get("count", 0)
            paginator = Paginator(app_list, req.limit)
            paginator.count = count
            context['result_list'] = app_list
            context['is_paginated'] = count > 0
            context['page_obj'] = paginator.page(req.offset)
            context['paginator'] = paginator
        except Exception as e:
            logger.error(e)
        return context


class DevopsFlowCreateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "flow_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            context['version_list'] = []
            context['app_info'] = {}
            context['is_add'] = 1
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            addAppResults = hu.post(serivceName="job", restName="/rest/flowcontrol/add/", datas=reqData)
            addAppResults = addAppResults.json()
            if addAppResults['status'] == 'SUCCESS':
                result['status'] = 0
                result['msg'] = '保存应用信息成功'
            else:
                result['status'] = 1
                result['msg'] = '保存应用信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '保存异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')


class DevopsFlowUpdateView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "flow_form.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            id = kwargs.get('pk', 0)
            hu = HttpUtils(self.request)
            app_list_result = hu.get(serivceName="job", restName="/rest/flowcontrol/list/", datas={'id':id})
            app_list = app_list_result.get("results", {})
            app = {}
            if len(app_list) > 0:
                app = app_list[0]
            context['app_info'] = app
            context['is_add'] = 0
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            app_id = reqData.get("id", None)
            if app_id:
                del reqData['offset']
                del reqData['limit']
                del reqData['csrfmiddlewaretoken']
                addAppResults = hu.post(serivceName="job", restName="/rest/flowcontrol/update/", datas=reqData)
                addAppResults = addAppResults.json()
                if addAppResults['status'] == 'SUCCESS':
                    result['status'] = 0
                    result['msg'] = '更新流量调度信息成功'
                else:
                    result['status'] = 1
                    result['msg'] = '更新流量调度信息失败'
            else:
                result['status'] = 1
                result['msg'] = '更新流量调度信息失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '更新异常'
            logger.error(e)
        return HttpResponse(json.dumps(result), content_type='application/json')


class DevopsFlowOperationView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
    template_name = "flow_operation.html"

    def get_context_data(self, **kwargs):
        context = {}
        try:
            req = self.request
            hu = HttpUtils(req)
            id = kwargs.get('pk',0)
            reqData = hu.getRequestParam()
            name = reqData.get('name',"")
            toolId = reqData.get('toolId')
            commandId = reqData.get('commandId',0)
            if not commandId or commandId == "None":
                commandId = 0
            commandLineId = reqData.get('commandLineId',0)
            if not commandLineId or commandLineId == "None":
                commandLineId = 0
            getData = {'offset': 0, 'limit': 1000, 'is_enabled': 1}
            hostgroupResult = hu.get(serivceName="cmdb", restName="/rest/hostgroup/list_tree/", datas=getData)
            tool_list_result = hu.get(serivceName="job", restName="/rest/job/list_tool_set/",datas={'id':toolId})
            tool_list = tool_list_result.get("results", [])
            tool = {}
            if len(tool_list) > 0:
                for tool in tool_list:
                    tool['param'] = json.loads(tool['param'])
                    del tool['is_enabled']
                tool = tool_list[0]

            context["result_dict"] = {}
            context['hostGroup_list'] = hostgroupResult.get("data", [])
            context['tool_info'] = tool
            context['commandId'] = commandId
            context['commandLineId'] = commandLineId
            context['name'] = name
        except Exception as e:
            logger.error(e)
        return context

    def post_ajax(self, request, *args, **kwargs):
        result = {'status': 0}
        try:
            hu = HttpUtils(self.request)
            reqData = hu.getRequestParam()
            commandSetId = int(reqData.get("command_set_id", 0))
            command_info = reqData.get("command_info", None)
            deploy_info = reqData.get("deploy_info", None)
            if commandSetId == 0 and command_info:
                jobAddResults = hu.post(serivceName="job", restName="/rest/job/add/", datas=command_info)
                jobAddResults = jobAddResults.json()
                if (jobAddResults["status"] == "FAILURE"):
                    logger.error("创建调度job失败")
                else:
                    data = jobAddResults["data"]
                    deploy_info = {}
                    step = json.loads(command_info)['steps'][0]
                    line = step['lines'][0]
                    for k in data:
                        commandSetId = k
                        deploy_info['command_set_id'] = k
                        deploy_info['new_flow'] = 1
                        deploy_info['paras'] = {
                            1: {
                                "target_type": step['target_type'],
                                "target_group_ids": step['target_group_ids'],
                                "target_host_list": step['target_host_list'],
                                "go_live": step['go_live']
                            }
                        }
                        step_ids = data[k]
                        step = step_ids[0]
                        for k2 in step:
                            line_id = step[k2][0]
                            deploy_info['paras'][1][line_id] = {
                                "parameter": line['default_script_parameter'],
                                "is_skip": 0
                            }
                            id = kwargs.get('pk', 0)
                            addAppResults = hu.post(serivceName="job", restName="/rest/flowcontrol/update/",
                                                    datas={'id': id, "command_set_id": commandSetId,
                                                           'command_line_id': line_id})
                            addAppResults = addAppResults.json()
                            if addAppResults['status'] == 'FAILURE':
                                deploy_info = None
            if deploy_info:
                runResults = hu.post(serivceName="job", restName="/rest/job/run/", datas=deploy_info)
                runJson = runResults.json()
                if int(runJson.get("job_id", 0)) > 0:
                    result["status"] = "0"
                else:
                    result["status"] = "1"
                    result['msg'] = '调度执行失败'
                result['job_id'] = runJson.get("job_id", 0)
                result['set_id'] = commandSetId
            else:
                result['status'] = 1
                result['msg'] = '没有调度执行信息，调度失败'
        except Exception as e:
            result['status'] = 1
            result['msg'] = '调度异常'
            logger.error(e)
        return HttpResponse(json.dumps(result),content_type='application/json')

class DevopsFlowReportView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, TemplateView):
    template_name = "flow_report.html"
    def get_context_data(self, **kwargs):
        context = super(DevopsFlowReportView, self).get_context_data(**kwargs)
        try:
            hu = HttpUtils(self.request)
            ec_grafana_graph_result = hu.get(serivceName="job", restName="/rest/deploy/ec_grafana_graph/", datas={})
            context['result'] = ec_grafana_graph_result.get('data',[])
        except Exception as e:
            logging.error(e)
        return context

# class DevopsFlowReportView(LoginRequiredMixin, JSONResponseMixin,AjaxResponseMixin, TemplateView):
#     template_name = "flow_report.html"
#
#     def get_context_data(self, **kwargs):
#         context = {}
#         try:
#             hu = HttpUtils(self.request)
#             dashboard = hu.get_url("http://172.29.164.91:3000/d/qJbknE7mk/dashboard?orgId=1",datas={},auth=("admin","admin"))
#             #datas = json.dumps({"user":"admin","password":"admin"})
#             #html = requests.post("http://172.29.164.91:3000/login", data=datas.encode('UTF-8'),headers={"Content-Type": "application/json", "Accept-Language": "zh-CN,zh;q=0.8",}, timeout=10000)
#             #result_cookies = requests.utils.dict_from_cookiejar(html.cookies)
#             html = dashboard.text
#             html = html.replace('href="public', 'href="http://172.29.164.91:3000/public')
#             html = html.replace('src="public', 'href="http://172.29.164.91:3000/public')
#             context['html'] = html
#         except Exception as e:
#             logger.error(e)
#         return context
#
#
# def DevopsFlowReportView2(request):
#     try:
#         datas = json.dumps({"user": "admin", "password": "admin"})
#         html = requests.post("http://172.29.164.91:3000/login", data=datas.encode('UTF-8'),
#                              headers={"Content-Type": "application/json", "Accept-Language": "zh-CN,zh;q=0.8", },
#                              timeout=10000)
#         result_cookies = requests.utils.dict_from_cookiejar(html.cookies)
#         response = render(request, "flow_report.html", {})
#         response['Access-Control-Allow-Origin'] = "*"
#         response.set_cookie("grafana_remember",result_cookies['grafana_remember'])
#         response.set_cookie("grafana_sess", result_cookies['grafana_sess'])
#         response.set_cookie("grafana_user", result_cookies['grafana_user'])
#     except Exception as e:
#         logger.error(e)
#     return response




